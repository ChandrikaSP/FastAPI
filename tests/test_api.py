from fastapi.testclient import TestClient
from app.main import app
import time

client = TestClient(app)

def test_risk_workflow():
    # Step 1: Create a risk
    risk_data = {
        "title": "Oil Spill",
        "description": "Leakage near storage unit",
        "category": "Environmental",
    }

    response = client.post("/risks", json=risk_data)
    assert response.status_code == 201   #If the response is anything else (like 500), the test fails here.

    data = response.json()   #extract the JSON response body.
    assert data["title"] == "Oil Spill"    #check: Is the title correct? Is the status initially set to "in process"? If either value doesn't match, AssertionError is raised
    assert data["status"] == "in process"
    risk_id = data["id"]

    # Step 2: Immediately fetch the risk
    r = client.get(f"/risks/{risk_id}")
    assert r.status_code == 200
    assert r.json()["status"] in ["in process", "completed"]  # may vary if async status is either "in process" or "completed" – because the background job might have finished (or not) depending on timing.

    # Step 3: Wait 11 seconds for background workflow to complete
    time.sleep(11)


    # Step 4: Check status again
    r2 = client.get(f"/risks/{risk_id}")
    assert r2.status_code == 200
    assert r2.json()["status"] == "completed"

def test_list_risks():
    r = client.get("/risks")
    assert r.status_code == 200
    risks = r.json()
    assert isinstance(risks, list)
    assert all("id" in r for r in risks)

########################################################## old code ################################################################

# def test_risk_workflow():
#     risk_data = {
#         "title": "Oil Spill",
#         "description": "Leakage near storage unit",
#         "category": "Environmental",
#     }
#     response = client.post("/risks", json=risk_data)
#     assert response.status_code == 201
#     data = response.json()
#     assert data["title"] == "Oil Spill"
#     assert data["status"] == "in process"
#     risk_id = data["id"]

#     r = client.get(f"/risks/{risk_id}")
#     assert r.status_code == 200
#     assert r.json()["status"] in ["in process", "completed"]

#     time.sleep(11)

#     r2 = client.get(f"/risks/{risk_id}")
#     assert r2.status_code == 200
#     assert r2.json()["status"] == "completed"

# def test_list_risks():
#     r = client.get("/risks")
#     assert r.status_code == 200
#     risks = r.json()
#     assert isinstance(risks, list)
#     assert all("id" in r for r in risks)
