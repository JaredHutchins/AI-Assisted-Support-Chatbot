

"""
Minimal Flask entry point for the AI-Assisted Support Chatbot (ASC).

This file exists to prove:
- the environment is set up correctly
- Flask runs without errors
- we have a clean baseline to build on

Nothing fancy here. This is intentional.
"""


from flask import Flask, render_template, request
from app.routes.session_routes import session_routes


 # NOTE:
 # This file is intentionally minimal.
 # Core session logic, state handling, and resolution or escalation decisions
 # must live outside this file to avoid coupling Flask with domain logic.
def create_app() -> Flask:
    """
    Application factory.

    Using a factory keeps setup predictable and makes the app easier
    to test and extend later without refactoring.
    """
    app = Flask(__name__)
    app.register_blueprint(session_routes)

    @app.route("/")
    def healthCheck():
        """
        Simple sanity check.

        If this route loads in a browser, Flask is running and
        the project wiring is correct.
        """
        return "ASC is running."

    @app.route("/session", methods=["GET", "POST"])
    def session_view():
        """
        Minimal agent UI.

        Allows a support agent to start a session and view the
        current runtime state. Presentation only.
        """
        current_state = None

        if request.method == "POST":
            session_id = request.form.get("sessionId", "demo1")

            # Call the API route internally
            from app.session_context import SessionContext
            ctx = SessionContext(session_id)
            ctx.advanceState("Idle")
            current_state = "Idle"

        return render_template("session.html", current_state=current_state)

    return app


if __name__ == "__main__":
    """
    Local development entry point.

    Debug is enabled for fast feedback during development.
    This will be turned off or configured differently later.
    """
    app = create_app()
    app.run(debug=True)