

"""
Minimal Flask entry point for the AI-Assisted Support Chatbot (ASC).

This file exists to prove:
- the environment is set up correctly
- Flask runs without errors
- we have a clean baseline to build on

Nothing fancy here. This is intentional.
"""

from flask import Flask


def create_app() -> Flask:
    """
    Application factory.

    Using a factory keeps setup predictable and makes the app easier
    to test and extend later without refactoring.
    """
    app = Flask(__name__)

    @app.route("/")
    def health_check():
        """
        Simple sanity check.

        If this route loads in a browser, Flask is running and
        the project wiring is correct.
        """
        return "ASC is running."

    return app


if __name__ == "__main__":
    """
    Local development entry point.

    Debug is enabled for fast feedback during development.
    This will be turned off or configured differently later.
    """
    app = create_app()
    app.run(debug=True)