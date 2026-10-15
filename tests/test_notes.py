def create_note(client, title, content="", tags=None):
    return client.post(
        "/notes/",
        json={
            "title": title,
            "content": content,
            "tags": tags or [],
        },
    )


def test_create_note(client):
    response = create_note(
        client,
        "Python Basics",
        "Learning Python",
        ["Programming"],
    )

    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Python Basics"
    assert "programming" in data["tags"]


def test_duplicate_title_rejected(client):
    create_note(client, "Python Basics")

    response = create_note(client, "Python Basics")

    assert response.status_code == 409


def test_automatic_link_and_backlink(client):
    target = create_note(client, "Data Structures").json()

    source_response = create_note(
        client,
        "Learning C++",
        "Studying [[Data Structures]].",
    )

    assert source_response.status_code == 201
    assert source_response.json()["linked_notes"][0]["id"] == target["id"]

    target_response = client.get(f"/notes/{target['id']}")

    assert target_response.status_code == 200
    backlinks = target_response.json()["backlinks"]
    assert any(note["title"] == "Learning C++" for note in backlinks)


def test_self_link_rejected(client):
    note = create_note(client, "Python Basics").json()

    response = client.patch(
        f"/notes/{note['id']}/link",
        json={"target_id": note["id"]},
    )

    assert response.status_code == 409


def test_duplicate_link_rejected(client):
    source = create_note(client, "Source").json()
    target = create_note(client, "Target").json()

    payload = {"target_id": target["id"]}

    first = client.patch(
        f"/notes/{source['id']}/link",
        json=payload,
    )
    second = client.patch(
        f"/notes/{source['id']}/link",
        json=payload,
    )

    assert first.status_code == 201
    assert second.status_code == 409


def test_missing_note_returns_404(client):
    response = client.get("/notes/999999")

    assert response.status_code == 404


def test_tag_filter_and_keyword_search(client):
    create_note(
        client,
        "Python Basics",
        "Variables and functions",
        ["Programming"],
    )
    create_note(
        client,
        "Daily Planning",
        "Organize tasks",
        ["Productivity"],
    )

    tag_response = client.get("/notes/?tag=PROGRAMMING")
    assert tag_response.status_code == 200
    assert [n["title"] for n in tag_response.json()] == ["Python Basics"]

    search_response = client.get("/notes/?keyword=Variables")
    assert search_response.status_code == 200
    assert [n["title"] for n in search_response.json()] == ["Python Basics"]


def test_graph_returns_nodes_and_edges(client):
    source = create_note(client, "Source").json()
    target = create_note(client, "Target").json()

    client.patch(
        f"/notes/{source['id']}/link",
        json={"target_id": target["id"]},
    )

    response = client.get("/graph/")

    assert response.status_code == 200
    data = response.json()
    assert len(data["nodes"]) == 2
    assert {
        "source": source["id"],
        "target": target["id"],
    } in data["edges"]