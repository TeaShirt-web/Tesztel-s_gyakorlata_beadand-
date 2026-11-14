"""Lépésdefiníciók az osszegzes.feature fájlhoz (behave)."""

from behave import given, when, then


@given("az alkalmazás fut és még nincs beküldött szám")
def step_ures_alkalmazas(context):
    context.client.post("/reset")


@when("beküldöm a {szam:d} számot")
def step_szam_bekuldese(context, szam):
    context.response = context.client.post("/numbers", json={"number": szam})
    assert context.response.status_code == 201, context.response.get_json()


@when('beküldöm a következő számokat: "{szamok}"')
def step_szamok_bekuldese(context, szamok):
    for resz in szamok.split(","):
        context.response = context.client.post(
            "/numbers", json={"number": int(resz.strip())}
        )
        assert context.response.status_code == 201


@when('beküldöm a "{szoveg}" szöveget számként')
def step_szoveg_bekuldese(context, szoveg):
    context.response = context.client.post("/numbers", json={"number": szoveg})


@when("lekérdezem az összeget")
def step_osszeg_lekerdezese(context):
    context.response = context.client.get("/sum")


@then("a válasz státuszkódja {kod:d}")
def step_statuszkod(context, kod):
    assert context.response.status_code == kod, (
        f"Várt: {kod}, kapott: {context.response.status_code}"
    )


@then("az összeg {osszeg:d}")
def step_osszeg(context, osszeg):
    adat = context.response.get_json()
    assert adat == {"sum": osszeg}, f"Várt összeg: {osszeg}, kapott: {adat}"
