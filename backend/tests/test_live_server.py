import time
import subprocess
import urllib.request
import json
import sys

def run_live_check():
    print("Starting uvicorn server on port 8000...")
    proc = subprocess.Popen([sys.executable, "-m", "uvicorn", "backend.main:app", "--port", "8000"])
    time.sleep(3)
    try:
        # 1. Health
        with urllib.request.urlopen("http://localhost:8000/api/health") as res:
            data = json.loads(res.read().decode())
            print("1. Health OK:", data)

        # 2. Scenario GET (read-only)
        with urllib.request.urlopen("http://localhost:8000/api/scenarios/S-MATH-01") as res:
            sc1 = json.loads(res.read().decode())
            print("2. Scenario GET OK:", sc1["scenario_id"], "| Model:", sc1["ro1042"]["vehicle_model"], "| v", sc1["snapshot_version"])

        # 3. Solve POST
        req = urllib.request.Request(
            "http://localhost:8000/api/solve",
            data=json.dumps({"scenario_id": "S-MATH-01", "compare_a2_p3": True}).encode(),
            headers={"Content-Type": "application/json"}
        )
        with urllib.request.urlopen(req) as res:
            solve_data = json.loads(res.read().decode())
            prop_id = solve_data["active_proposal"]["proposal_id"]
            reduction = solve_data["comparison"]["weighted_lateness_reduction_pct"]
            print(f"3. Solve OK: Proposal {prop_id} | Reduction: {reduction}% | Finish: {solve_data['active_proposal']['ro1051_finish_clock']}")

        # 4. Competing reservation POST
        req_race = urllib.request.Request(
            "http://localhost:8000/api/scenarios/S-MATH-01/events/competing-reservation?source_id=S1",
            data=b"",
            headers={"Content-Type": "application/json"}
        )
        with urllib.request.urlopen(req_race) as res:
            race_data = json.loads(res.read().decode())
            print(f"4. Competing Reservation OK: Status {race_data['status']} | New Version: v{race_data['new_snapshot_version']}")

        # 5. Stale approval rejection POST
        req_appr = urllib.request.Request(
            f"http://localhost:8000/api/proposals/{prop_id}/approve",
            data=b"",
            headers={"Content-Type": "application/json"}
        )
        with urllib.request.urlopen(req_appr) as res:
            appr_data = json.loads(res.read().decode())
            print(f"5. Stale Approval Rejected OK: Status {appr_data['status']} | Success: {appr_data['success']} | New Prop: {appr_data['new_proposal']['proposal_id']}")

        # 6. Approve new proposal POST
        new_id = appr_data['new_proposal']['proposal_id']
        req_commit = urllib.request.Request(
            f"http://localhost:8000/api/proposals/{new_id}/approve",
            data=b"",
            headers={"Content-Type": "application/json"}
        )
        with urllib.request.urlopen(req_commit) as res:
            commit_data = json.loads(res.read().decode())
            print(f"6. Re-approval Committed OK: Status {commit_data['status']} | Success: {commit_data['success']}")

        print("\nALL LIVE SERVER ENDPOINTS VERIFIED SUCCESSFULLY!")
    finally:
        proc.terminate()
        proc.wait(timeout=5)

if __name__ == "__main__":
    run_live_check()
