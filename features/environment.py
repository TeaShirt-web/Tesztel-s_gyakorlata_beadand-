"""behave környezet: minden scenario előtt friss alkalmazás és test client."""

from app import create_app


def before_scenario(context, scenario):
    app = create_app()
    app.config["TESTING"] = True
    context.client = app.test_client()
    context.response = None
