"""
Unit tesztek a Szám-összegző REST API-hoz (TDD).

Ezek a tesztek az implementáció ELŐTT készültek (test-first), AI segítségével.
Az elvárt interfész:
  - app.py-ban egy NumberStore osztály: add(number), total(), reset()
  - app.py-ban egy create_app() factory, ami Flask alkalmazást ad vissza
  - POST /numbers   body: {"number": <egész szám>}  -> 201
  - GET  /sum       -> 200, {"sum": <összeg>}
  - POST /reset     -> 200, a tárolt számok törlése

Futtatás:  pytest test_app.py -v
"""

import pytest

from app import NumberStore, create_app


# ---------------------------------------------------------------------------
# A belső logika (NumberStore) unit tesztjei
# ---------------------------------------------------------------------------

def test_ures_tarolo_osszege_nulla():
    store = NumberStore()
    assert store.total() == 0


def test_szamok_osszeadodnak():
    store = NumberStore()
    store.add(5)
    store.add(10)
    store.add(-3)
    assert store.total() == 12


def test_reset_kiuriti_a_tarolot():
    store = NumberStore()
    store.add(42)
    store.reset()
    assert store.total() == 0


@pytest.mark.parametrize("hibas_ertek", [3.14, "5", None, True, [1, 2]])
def test_nem_egesz_szam_eseten_hiba(hibas_ertek):
    store = NumberStore()
    with pytest.raises(TypeError):
        store.add(hibas_ertek)
    assert store.total() == 0


# ---------------------------------------------------------------------------
# Az API végpontok tesztjei (Flask test client)
# ---------------------------------------------------------------------------

@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_kezdeti_osszeg_nulla(client):
    response = client.get("/sum")
    assert response.status_code == 200
    assert response.get_json() == {"sum": 0}


def test_szam_bekuldese_201_valaszt_ad(client):
    response = client.post("/numbers", json={"number": 7})
    assert response.status_code == 201
    assert response.get_json()["number"] == 7


def test_bekuldott_szamok_osszege(client):
    for n in (1, 2, 3, 4):
        client.post("/numbers", json={"number": n})
    response = client.get("/sum")
    assert response.get_json() == {"sum": 10}


@pytest.mark.parametrize(
    "body",
    [{"number": "abc"}, {"number": 1.5}, {"szam": 5}, {}, {"number": True}],
)
def test_hibas_keres_400_valaszt_ad(client, body):
    response = client.post("/numbers", json=body)
    assert response.status_code == 400
    assert "error" in response.get_json()
    assert client.get("/sum").get_json() == {"sum": 0}


def test_reset_vegpont_nullazza_az_osszeget(client):
    client.post("/numbers", json={"number": 100})
    response = client.post("/reset")
    assert response.status_code == 200
    assert client.get("/sum").get_json() == {"sum": 0}
