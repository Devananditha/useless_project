import time
import subprocess
import urllib.request
import json
import sys

def post_json(url: str, data: dict = None) -> dict:
    payload = json.dumps(data).encode("utf-8") if data is not None else b""
    req = urllib.request.Request(
        url,
        data=payload,
        headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req) as res:
        return json.loads(res.read().decode("utf-8"))

def get_json(url: str) -> dict:
    with urllib.request.urlopen(url) as res:
        return json.loads(res.read().decode("utf-8"))

def wait_for_endpoint(url: str, timeout: float = 12.0):
    start = time.time()
    last_err = None
    while time.time() - start < timeout:
        try:
            with urllib.request.urlopen(url) as res:
                if res.status == 200:
                    return
        except Exception as e:
            last_err = e
            time.sleep(0.5)
    raise TimeoutError(f"Endpoint {url} not ready within {timeout}s: {last_err}")


def run_live_check():
    print("Starting uvicorn server on port 8000...")
    proc = subprocess.Popen([sys.executable, "-m", "uvicorn", "backend.main:app", "--host", "127.0.0.1", "--port", "8000"])
    try:
        wait_for_endpoint("http://127.0.0.1:8000/api/health", timeout=12.0)
        # 1. Health GET
        health = get_json("http://127.0.0.1:8000/api/health")
        assert health["status"] == "healthy", f"Health status unexpected: {health}"
        print(f"1. Health OK: {health}")

        # 2. Scenario Select POST (Act 1: Canonical S-MATH-01)
        sel_res = post_json("http://127.0.0.1:8000/api/scenarios/S-MATH-01/select")
        assert sel_res["active_scenario_id"] == "S-MATH-01", f"Scenario select failed: {sel_res}"
        print(f"2. Scenario Select POST OK: {sel_res['active_scenario_id']} | v{sel_res['snapshot']['snapshot_version']}")

        # 3. Scenario Read-Only GET
        sc1 = get_json("http://127.0.0.1:8000/api/scenarios/S-MATH-01")
        assert sc1["scenario_id"] == "S-MATH-01"
        assert sc1["snapshot_version"] == sel_res["snapshot"]["snapshot_version"], "GET mutated snapshot version!"
        print(f"3. Scenario Read-Only GET OK: {sc1['scenario_id']} | Model: {sc1['ro1042']['vehicle_model']} | v{sc1['snapshot_version']}")

        # 4. Act 1 Solve POST (Canonical: Immobilized -> HOLD_ON_BAY, S1)
        solve_res1 = post_json("http://127.0.0.1:8000/api/solve", {"scenario_id": "S-MATH-01", "compare_a2_p3": True})
        act1_prop = solve_res1["active_proposal"]
        act1_prop_id = act1_prop["proposal_id"]
        assert act1_prop["selected_movement"] == "HOLD_ON_BAY"
        assert act1_prop["selected_source_id"] == "S1"
        assert act1_prop["weighted_lateness_ticks"] == 33.0
        assert solve_res1["comparison"]["weighted_lateness_reduction_pct"] == 66.7
        print(f"4. Act 1 Solve OK: Prop {act1_prop_id} | Move: {act1_prop['selected_movement']} | Source: {act1_prop['selected_source_id']} | Reduction: {solve_res1['comparison']['weighted_lateness_reduction_pct']}% | RO-1051 Finish: {act1_prop['ro1051_finish_clock']}")

        # 5. Act 2 Scenario Select POST (Rollable: S-MATH-01-ROLLABLE)
        sel_roll = post_json("http://127.0.0.1:8000/api/scenarios/S-MATH-01-ROLLABLE/select")
        assert sel_roll["active_scenario_id"] == "S-MATH-01-ROLLABLE"
        print(f"5. Act 2 Scenario Select POST OK: {sel_roll['active_scenario_id']} | v{sel_roll['snapshot']['snapshot_version']}")

        # 6. Cross-Scenario Approval Rejection POST
        # Attempting to approve Act 1 proposal (for S-MATH-01) while S-MATH-01-ROLLABLE is active
        cross_res = post_json(f"http://127.0.0.1:8000/api/proposals/{act1_prop_id}/approve")
        assert cross_res["success"] is False
        assert cross_res["status"] == "SCENARIO_MISMATCH"
        assert "Scenario mismatch" in cross_res["message"]
        print(f"6. Cross-Scenario Approval Rejection OK: Status: {cross_res['status']} | Message: {cross_res['message']}")

        # 7. Act 2 Solve POST (Rollable -> RELOCATE_TO_H2, S2)
        solve_res2 = post_json("http://127.0.0.1:8000/api/solve", {"scenario_id": "S-MATH-01-ROLLABLE", "compare_a2_p3": True})
        act2_prop = solve_res2["active_proposal"]
        act2_prop_id = act2_prop["proposal_id"]
        assert act2_prop["selected_movement"] == "RELOCATE_TO_H2"
        assert act2_prop["selected_source_id"] == "S2"
        assert act2_prop["weighted_lateness_ticks"] == 1.0  # 1 tick lateness (finish 67 - promise 66)
        assert solve_res2["comparison"]["weighted_lateness_reduction_pct"] == 99.0  # (99 - 1) / 99 = 99.0%
        print(f"7. Act 2 Solve OK: Prop {act2_prop_id} | Move: {act2_prop['selected_movement']} | Source: {act2_prop['selected_source_id']} | Reduction: {solve_res2['comparison']['weighted_lateness_reduction_pct']}% | Weighted Lateness: {act2_prop['weighted_lateness_ticks']} ticks")

        # 8. Act 2 Approval POST
        appr_roll = post_json(f"http://127.0.0.1:8000/api/proposals/{act2_prop_id}/approve")
        assert appr_roll["success"] is True
        assert appr_roll["status"] == "APPROVED"
        print(f"8. Act 2 Proposal Approved OK: Status: {appr_roll['status']} | Success: {appr_roll['success']}")

        # 8b. Idempotency Check: Repeated approval of already committed proposal
        repeat_appr = post_json(f"http://127.0.0.1:8000/api/proposals/{act2_prop_id}/approve")
        assert repeat_appr["success"] is True
        assert repeat_appr["status"] == "ALREADY_APPROVED"
        print(f"8b. Idempotent Approval OK: Status: {repeat_appr['status']} | Success: {repeat_appr['success']}")

        # 8c. Independent Verification Endpoint POST
        verify_roll = post_json(f"http://127.0.0.1:8000/api/proposals/{act2_prop_id}/verify")
        assert verify_roll["status"] == "VERIFIED"
        assert verify_roll["verification"]["certificate_id"].startswith("CERT-")
        print(f"8c. Proposal Verification Endpoint OK: Cert ID: {verify_roll['verification']['certificate_id']} | Status: {verify_roll['status']}")

        # 9. Switch back to Act 1 for Stock Race Test
        post_json("http://127.0.0.1:8000/api/scenarios/S-MATH-01/select")
        solve_act1_fresh = post_json("http://127.0.0.1:8000/api/solve", {"scenario_id": "S-MATH-01", "compare_a2_p3": True})
        fresh_prop_id = solve_act1_fresh["active_proposal"]["proposal_id"]
        assert solve_act1_fresh["active_proposal"]["selected_source_id"] == "S1"
        print(f"9. Reset to Act 1 Solve OK: Fresh Prop {fresh_prop_id} targeting S1")

        # 10. Act 3 Competing Reservation POST (Source S1 allocated elsewhere)
        race_res = post_json("http://127.0.0.1:8000/api/scenarios/S-MATH-01/events/competing-reservation?source_id=S1")
        assert race_res["status"] == "COMPETING_RESERVATION_SIMULATED"
        assert race_res["affected_source"] == "S1"
        assert race_res["new_atp"] == 0
        assert race_res["new_snapshot_version"] == 15
        print(f"10. Act 3 Competing Reservation OK: Status: {race_res['status']} | Affected Source: {race_res['affected_source']} | Version incremented: v{race_res['new_snapshot_version']}")

        # 11. Stale Proposal Rejection POST
        stale_res = post_json(f"http://127.0.0.1:8000/api/proposals/{fresh_prop_id}/approve")
        assert stale_res["success"] is False
        assert stale_res["status"] == "STALE_SNAPSHOT"
        fallback_prop = stale_res["new_proposal"]
        assert fallback_prop is not None
        assert fallback_prop["selected_source_id"] == "S2"
        print(f"11. Stale Proposal Rejection OK: Status: {stale_res['status']} | Fallback Prop {fallback_prop['proposal_id']} generated with Source {fallback_prop['selected_source_id']}")

        # 12. Re-Approval of Replacement Proposal POST
        commit_res = post_json(f"http://127.0.0.1:8000/api/proposals/{fallback_prop['proposal_id']}/approve")
        assert commit_res["success"] is True
        assert commit_res["status"] == "APPROVED"
        print(f"12. Replacement Proposal Approved OK: Status: {commit_res['status']} | Success: {commit_res['success']}")

        # 13. HTTP Black-Box Rejection: Non-existent / invalid proposal ID
        invalid_res = post_json("http://127.0.0.1:8000/api/proposals/PROP-DOES-NOT-EXIST/approve")
        assert invalid_res["success"] is False
        assert invalid_res["status"] == "NOT_FOUND"
        print(f"13. HTTP Unknown Proposal Refusal OK: Status: {invalid_res['status']}")

        print("\n=======================================================")
        print("ALL LIVE SERVER ENDPOINTS & WORKFLOWS VERIFIED 100% OK!")
        print("=======================================================\n")
    finally:
        proc.terminate()
        proc.wait(timeout=5)

if __name__ == "__main__":
    run_live_check()
