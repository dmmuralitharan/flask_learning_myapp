def test_create_todo(client):
    response = client.post("/api/v1/todos/", json={"task": "Test task"})
    assert response.status_code == 200
    data = response.get_json()
    assert data["data"]["task"] == "Test task"
    assert data["data"]["completed"] is False


def test_get_todos(client):
    client.post("/api/v1/todos/", json={"task": "Sample 1"})
    client.post("/api/v1/todos/", json={"task": "Sample 2"})

    response = client.get("/api/v1/todos/")
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data["data"], list)
    assert len(data["data"]) >= 2


def test_update_todo(client):
    res = client.post("/api/v1/todos/", json={"task": "Old Task"})
    todo_id = res.get_json()["data"]["id"]

    response = client.put(
        f"/api/v1/todos/{todo_id}", json={"task": "Updated", "completed": True}
    )
    assert response.status_code == 200
    data = response.get_json()
    assert data["data"]["task"] == "Updated"


def test_delete_todo(client):
    res = client.post("/api/v1/todos/", json={"task": "To Delete"})
    todo_id = res.get_json()["data"]["id"]

    response = client.delete(f"/api/v1/todos/{todo_id}")
    assert response.status_code == 200
