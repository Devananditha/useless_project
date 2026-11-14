import time
import subprocess
import urllib.request
import json
import sys
import os

def wait_for_endpoint(url: str, timeout: float = 10.0):
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

def test_full_stack():
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    print(f"Repo root: {repo_root}")
    
    print("1. Starting backend uvicorn on 127.0.0.1:8000...")
    backend_proc = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "backend.main:app", "--host", "127.0.0.1", "--port", "8000"],
        cwd=repo_root
    )
    
    print("2. Starting frontend vite on 127.0.0.1:5173...")
    frontend_proc = subprocess.Popen(
        ["npm", "run", "dev", "--", "--port", "5173", "--host", "127.0.0.1"],
        cwd=os.path.join(repo_root, "frontend"),
        shell=True
    )
    
    try:
        print("Waiting for backend uvicorn to respond...")
        wait_for_endpoint("http://127.0.0.1:8000/api/health", timeout=12.0)
        print("Backend uvicorn is responding on 127.0.0.1:8000!")

        print("Waiting for Vite dev server to respond...")
        wait_for_endpoint("http://127.0.0.1:5173/", timeout=12.0)
        print("Vite dev server is responding on 127.0.0.1:5173!")

        # 3. Check Vite HTML
        print("3. Checking Vite HTML...")
        with urllib.request.urlopen("http://127.0.0.1:5173/") as res:
            html = res.read().decode("utf-8")
            assert "<div id=\"root\"></div>" in html or "vite" in html.lower()
            print("   Vite frontend served HTML successfully!")

        # 4. Check Vite Proxy to backend
        print("4. Testing Vite API proxy at http://127.0.0.1:5173/api/health...")
        with urllib.request.urlopen("http://127.0.0.1:5173/api/health") as res:
            data = json.loads(res.read().decode("utf-8"))
            assert data["status"] == "healthy", f"Unexpected proxy health response: {data}"
            print(f"   Vite Proxy to Backend OK: {data}")

        # 5. Test Act 1 through Vite Proxy
        print("5. Testing Act 1 Solve through Vite proxy...")
        req = urllib.request.Request(
            "http://127.0.0.1:5173/api/solve",
            data=json.dumps({"scenario_id": "S-MATH-01", "compare_a2_p3": True}).encode(),
            headers={"Content-Type": "application/json"}
        )
        with urllib.request.urlopen(req) as res:
            act1_data = json.loads(res.read().decode("utf-8"))
            assert act1_data["active_proposal"]["selected_source_id"] == "S1"
            assert act1_data["active_proposal"]["selected_movement"] == "HOLD_ON_BAY"
            assert act1_data["comparison"]["weighted_lateness_reduction_pct"] == 66.7
            print(f"   Act 1 through Proxy OK: Movement={act1_data['active_proposal']['selected_movement']}, Source={act1_data['active_proposal']['selected_source_id']}, Reduction={act1_data['comparison']['weighted_lateness_reduction_pct']}%")

        # 6. Test Act 2 through Vite Proxy
        print("6. Testing Act 2 Select & Solve through Vite proxy...")
        sel_req = urllib.request.Request("http://127.0.0.1:5173/api/scenarios/S-MATH-01-ROLLABLE/select", data=b"", headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(sel_req) as res:
            sel_data = json.loads(res.read().decode("utf-8"))
            assert sel_data["active_scenario_id"] == "S-MATH-01-ROLLABLE"
        
        req2 = urllib.request.Request(
            "http://127.0.0.1:5173/api/solve",
            data=json.dumps({"scenario_id": "S-MATH-01-ROLLABLE", "compare_a2_p3": True}).encode(),
            headers={"Content-Type": "application/json"}
        )
        with urllib.request.urlopen(req2) as res:
            act2_data = json.loads(res.read().decode("utf-8"))
            assert act2_data["active_proposal"]["selected_source_id"] == "S2"
            assert act2_data["active_proposal"]["selected_movement"] == "RELOCATE_TO_H2"
            assert act2_data["comparison"]["weighted_lateness_reduction_pct"] == 99.0
            print(f"   Act 2 through Proxy OK: Movement={act2_data['active_proposal']['selected_movement']}, Source={act2_data['active_proposal']['selected_source_id']}, Reduction={act2_data['comparison']['weighted_lateness_reduction_pct']}%")

        # 7. Test Act 3 Reset & Concurrency through Vite Proxy
        print("7. Testing Act 3 Stock Race & Concurrency through Vite proxy...")
        post_reset = urllib.request.Request("http://127.0.0.1:5173/api/reset", data=b"", headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(post_reset) as res:
            reset_data = json.loads(res.read().decode("utf-8"))
            assert reset_data["status"] == "RESET_SUCCESSFUL"

        # Solve Act 1 fresh
        req_fresh = urllib.request.Request(
            "http://127.0.0.1:5173/api/solve",
            data=json.dumps({"scenario_id": "S-MATH-01", "compare_a2_p3": True}).encode(),
            headers={"Content-Type": "application/json"}
        )
        with urllib.request.urlopen(req_fresh) as res:
            solve_fresh = json.loads(res.read().decode("utf-8"))
            act1_prop_id = solve_fresh["active_proposal"]["proposal_id"]

        # Trigger stock race
        req_race = urllib.request.Request(
            "http://127.0.0.1:5173/api/scenarios/S-MATH-01/events/competing-reservation?source_id=S1",
            data=b"",
            headers={"Content-Type": "application/json"}
        )
        with urllib.request.urlopen(req_race) as res:
            race_data = json.loads(res.read().decode("utf-8"))
            assert race_data["status"] == "COMPETING_RESERVATION_SIMULATED"
            assert race_data["new_atp"] == 0

        # Attempt stale approval
        req_stale = urllib.request.Request(
            f"http://127.0.0.1:5173/api/proposals/{act1_prop_id}/approve",
            data=b"",
            headers={"Content-Type": "application/json"}
        )
        with urllib.request.urlopen(req_stale) as res:
            stale_data = json.loads(res.read().decode("utf-8"))
            assert stale_data["status"] == "STALE_SNAPSHOT"
            assert stale_data["success"] is False
            assert stale_data["new_proposal"]["selected_source_id"] == "S2"
            print(f"   Act 3 Stale Rejection through Proxy OK: Status={stale_data['status']}, Fallback Source={stale_data['new_proposal']['selected_source_id']}")

        # Commit replacement proposal
        new_id = stale_data["new_proposal"]["proposal_id"]
        req_commit = urllib.request.Request(
            f"http://127.0.0.1:5173/api/proposals/{new_id}/approve",
            data=b"",
            headers={"Content-Type": "application/json"}
        )
        with urllib.request.urlopen(req_commit) as res:
            commit_data = json.loads(res.read().decode("utf-8"))
            assert commit_data["status"] == "APPROVED"
            assert commit_data["success"] is True
            print(f"   Act 3 Replacement Approval through Proxy OK: Status={commit_data['status']}")

        print("\n==========================================================================")
        print("ALL THREE ACTS VERIFIED 100% FUNCTIONAL THROUGH VITE DEVELOPMENT PROXY!")
        print("==========================================================================\n")
    finally:
        print("Cleaning up processes...")
        backend_proc.terminate()
        try:
            frontend_proc.terminate()
        except:
            pass
        subprocess.run(["taskkill", "/F", "/T", "/PID", str(backend_proc.pid)], capture_output=True)
        subprocess.run(["taskkill", "/F", "/T", "/PID", str(frontend_proc.pid)], capture_output=True)

if __name__ == "__main__":
    test_full_stack()
