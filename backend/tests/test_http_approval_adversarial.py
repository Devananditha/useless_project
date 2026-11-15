"""
HTTP-Level Adversarial Approval Route Acceptance Tests.
Executes against actual FastAPI ASGI HTTP routes via TestClient.
Verifies that no HTTP approval request can bypass independent verification,
tamper detection, scenario isolation, or optimistic concurrency versioning.
"""

import pytest
from fastapi.testclient import TestClient
from backend.main import app
from backend.state_store import store
from backend.models import ApprovalStatus, PolicyId
from backend.solver import solve_recovery_problem
from backend.verifier import verify_proposal, compute_proposal_digest, VerificationStatus

client = TestClient(app)


@pytest.fixture(autouse=True)
def isolated_reset():
    """Ensure clean store before and after each HTTP test."""
    store.reset_to_canonical()
    yield
    store.reset_to_canonical()


def test_http_1_rejected_proposal():
    """
    HTTP Test 1 — Rejected proposal:
    Generate a proposal, corrupt decision-relevant fields so verification rejects it,
    call the HTTP approval endpoint, and confirm approval is refused with REJECTED.
    """
    # 1. Generate proposal via HTTP solve
    solve_resp = client.post("/api/solve", json={"scenario_id": "S-MATH-01", "compare_a2_p3": False})
    assert solve_resp.status_code == 200
    prop_data = solve_resp.json()["active_proposal"]
    prop_id = prop_data["proposal_id"]

    # 2. Corrupt proposal state to REJECTED in store
    prop = store.get_proposal(prop_id)
    prop.approval_status = ApprovalStatus.REJECTED
    store.save_proposal(prop)

    # 3. Call normal HTTP approval endpoint
    appr_resp = client.post(f"/api/proposals/{prop_id}/approve")
    assert appr_resp.status_code == 200
    res = appr_resp.json()

    # 4. Confirm approval is refused
    assert res["success"] is False
    assert res["status"] == "REJECTED"
    assert "cannot be approved" in res["message"].lower()

    # Confirm proposal in store remains REJECTED
    saved = store.get_proposal(prop_id)
    assert saved.approval_status == ApprovalStatus.REJECTED


def test_http_2_missing_certificate():
    """
    HTTP Test 2 — Missing certificate:
    Generate a proposal, remove its verification certificate from the test store,
    call the HTTP approval endpoint, and confirm UNVERIFIED_PROPOSAL explicit rejection.
    """
    solve_resp = client.post("/api/solve", json={"scenario_id": "S-MATH-01", "compare_a2_p3": False})
    assert solve_resp.status_code == 200
    prop_id = solve_resp.json()["active_proposal"]["proposal_id"]

    # Strip certificate
    prop = store.get_proposal(prop_id)
    prop.verification_result = None
    prop.approval_status = ApprovalStatus.PENDING_APPROVAL
    store.save_proposal(prop)

    # Call HTTP approval route
    appr_resp = client.post(f"/api/proposals/{prop_id}/approve")
    assert appr_resp.status_code == 200
    res = appr_resp.json()

    assert res["success"] is False
    assert res["status"] == "UNVERIFIED_PROPOSAL"
    assert "lacks an independent verification certificate" in res["message"]

    saved = store.get_proposal(prop_id)
    assert saved.approval_status == ApprovalStatus.REJECTED


def test_http_3_insufficient_evidence():
    """
    HTTP Test 3 — Insufficient evidence:
    Generate a proposal with deliberately incomplete required evidence,
    attempt approval through HTTP, and confirm refusal with INSUFFICIENT_EVIDENCE.
    """
    solve_resp = client.post("/api/solve", json={"scenario_id": "S-MATH-01", "compare_a2_p3": False})
    assert solve_resp.status_code == 200
    prop_id = solve_resp.json()["active_proposal"]["proposal_id"]

    prop = store.get_proposal(prop_id)
    prop.verification_result = {
        "certificate_id": "CERT-TEST-INSUFF",
        "proposal_id": prop_id,
        "verification_status": VerificationStatus.INSUFFICIENT_EVIDENCE.value,
        "proposal_digest": compute_proposal_digest(prop),
        "checked_invariants": ["I1"],
        "violations": [],
        "verification_summary": "Missing interval evidence."
    }
    prop.approval_status = ApprovalStatus.INSUFFICIENT_EVIDENCE
    store.save_proposal(prop)

    appr_resp = client.post(f"/api/proposals/{prop_id}/approve")
    assert appr_resp.status_code == 200
    res = appr_resp.json()

    assert res["success"] is False
    assert res["status"] == "INSUFFICIENT_EVIDENCE"
    assert "cannot be authorized" in res["message"]

    saved = store.get_proposal(prop_id)
    assert saved.approval_status == ApprovalStatus.INSUFFICIENT_EVIDENCE


def test_http_4_tampered_after_verification():
    """
    HTTP Test 4 — Tampered after verification:
    Generate and verify a valid proposal, change its selected source or schedule intervals,
    call the HTTP approval endpoint, and confirm CERTIFICATE_TAMPERED refusal.
    """
    solve_resp = client.post("/api/solve", json={"scenario_id": "S-MATH-01", "compare_a2_p3": False})
    assert solve_resp.status_code == 200
    prop_id = solve_resp.json()["active_proposal"]["proposal_id"]

    # Tamper with decision field after certificate was created
    prop = store.get_proposal(prop_id)
    prop.selected_source_id = "S4"  # Changed source
    store.save_proposal(prop)

    appr_resp = client.post(f"/api/proposals/{prop_id}/approve")
    assert appr_resp.status_code == 200
    res = appr_resp.json()

    assert res["success"] is False
    assert res["status"] == "CERTIFICATE_TAMPERED"
    assert "modified after certificate generation" in res["message"]

    saved = store.get_proposal(prop_id)
    assert saved.approval_status == ApprovalStatus.REJECTED


def test_http_4b_tampered_schedule_interval():
    """
    HTTP Test 4b — Tampering with scheduled interval ticks post-certification.
    """
    solve_resp = client.post("/api/solve", json={"scenario_id": "S-MATH-01", "compare_a2_p3": False})
    assert solve_resp.status_code == 200
    prop_id = solve_resp.json()["active_proposal"]["proposal_id"]

    prop = store.get_proposal(prop_id)
    if prop.scheduled_intervals:
        prop.scheduled_intervals[0].end_tick += 5
    store.save_proposal(prop)

    appr_resp = client.post(f"/api/proposals/{prop_id}/approve")
    assert appr_resp.status_code == 200
    res = appr_resp.json()

    assert res["success"] is False
    assert res["status"] == "CERTIFICATE_TAMPERED"


def test_http_5_stale_snapshot():
    """
    HTTP Test 5 — Stale snapshot:
    Generate and verify a valid proposal, advance scenario snapshot via HTTP competing reservation,
    attempt approval through HTTP, confirm stale rejection and separately pending replacement proposal.
    """
    solve_resp = client.post("/api/solve", json={"scenario_id": "S-MATH-01", "compare_a2_p3": False})
    assert solve_resp.status_code == 200
    prop_id = solve_resp.json()["active_proposal"]["proposal_id"]

    # Advance snapshot version via HTTP
    race_resp = client.post("/api/scenarios/S-MATH-01/events/competing-reservation?source_id=S1")
    assert race_resp.status_code == 200
    assert race_resp.json()["new_snapshot_version"] == 15

    # Attempt to approve the original proposal
    appr_resp = client.post(f"/api/proposals/{prop_id}/approve")
    assert appr_resp.status_code == 200
    res = appr_resp.json()

    assert res["success"] is False
    assert res["status"] == "STALE_SNAPSHOT"
    assert res["requires_human_approval"] is True
    assert "new_proposal" in res

    # The replacement proposal must be distinct and pending approval
    new_prop = res["new_proposal"]
    assert new_prop["proposal_id"] != prop_id
    assert new_prop["approval_status"] == "PENDING_APPROVAL"
    assert new_prop["input_snapshot_version"] == 15


def test_http_5b_stale_status_cannot_transition_to_approved():
    """
    HTTP Test 5b — STALE_SNAPSHOT state can never transition to APPROVED.
    """
    solve_resp = client.post("/api/solve", json={"scenario_id": "S-MATH-01", "compare_a2_p3": False})
    assert solve_resp.status_code == 200
    prop_id = solve_resp.json()["active_proposal"]["proposal_id"]

    prop = store.get_proposal(prop_id)
    prop.approval_status = ApprovalStatus.STALE_SNAPSHOT
    store.save_proposal(prop)

    appr_resp = client.post(f"/api/proposals/{prop_id}/approve")
    assert appr_resp.status_code == 200
    res = appr_resp.json()

    assert res["success"] is False
    assert res["status"] == "STALE_SNAPSHOT"
    assert "cannot be approved" in res["message"].lower()

    saved = store.get_proposal(prop_id)
    assert saved.approval_status == ApprovalStatus.STALE_SNAPSHOT


def test_http_6_double_approval_idempotency():
    """
    HTTP Test 6 — Double approval:
    Approve a valid verified proposal through HTTP, submit the same approval request again,
    confirm ALREADY_APPROVED, and confirm no second PROPOSAL_COMMITTED event.
    """
    solve_resp = client.post("/api/solve", json={"scenario_id": "S-MATH-01", "compare_a2_p3": False})
    assert solve_resp.status_code == 200
    prop_id = solve_resp.json()["active_proposal"]["proposal_id"]

    # First approval
    first_appr = client.post(f"/api/proposals/{prop_id}/approve")
    assert first_appr.status_code == 200
    assert first_appr.json()["success"] is True
    assert first_appr.json()["status"] == "APPROVED"

    # Second approval
    second_appr = client.post(f"/api/proposals/{prop_id}/approve")
    assert second_appr.status_code == 200
    assert second_appr.json()["success"] is True
    assert second_appr.json()["status"] == "ALREADY_APPROVED"
    assert "already approved" in second_appr.json()["message"].lower()

    # Verify audit events via HTTP endpoint
    evts_resp = client.get("/api/events")
    assert evts_resp.status_code == 200
    all_events = evts_resp.json()["events"]
    commit_events = [
        e for e in all_events
        if e["event_type"] == "PROPOSAL_COMMITTED" and e.get("details", {}).get("proposal_id") == prop_id
    ]
    assert len(commit_events) == 1
