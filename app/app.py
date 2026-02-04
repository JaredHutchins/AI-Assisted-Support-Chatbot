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

# Demo knowledge base (deterministic, product-specific structure)
KNOWLEDGE_BASE = {
    "Widget A": {
        "Won't power on": [
            "Check power cable",
            "Check battery",
            "Check battery indicator LED"
        ],
        "Physical damage": [
            "Inspect device casing",
            "Check for cracked screen",
            "Verify device powers on at all"
        ],
        "Erratic behavior": [
            "Restart the device",
            "Check for recent drops or impacts",
            "Reset device settings"
        ]
    },
    "Widget B": {
        "Won't power on": [
            "Check power cable",
            "Check battery",
            "Check battery indicator LED"
        ],
        "Physical damage": [
            "Inspect device casing",
            "Check for cracked screen",
            "Verify device powers on at all"
        ],
        "Erratic behavior": [
            "Restart the device",
            "Check for recent drops or impacts",
            "Reset device settings"
        ]
    }
}


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
        Guided agent UI.

        Presentation-only workflow that demonstrates:
        - product selection
        - problem context
        - deterministic troubleshooting steps
        - resolution and escalation paths
        """
        # UI state defaults
        started = False
        escalated = False
        escalation_available = False

        product = None
        problem = None
        description = None

        step_index = 0
        attempted_steps = []
        current_step = None
        current_state = "Idle"

        if request.method == "POST":
            action = request.form.get("action")

            # Initial session start
            if action == "start":
                product = request.form.get("product")
                problem = request.form.get("problem")
                description = request.form.get("description")

                started = True
                step_index = 0
                attempted_steps = []

                current_step = KNOWLEDGE_BASE[product][problem][step_index]

            # Troubleshooting loop
            elif action == "not_resolved":
                product = request.form.get("product")
                problem = request.form.get("problem")
                description = request.form.get("description")
                step_index = int(request.form.get("step_index"))
                attempted_steps = request.form.getlist("attempted_steps")

                steps = KNOWLEDGE_BASE[product][problem]

                # Record the step that was just attempted
                if step_index < len(steps):
                    attempted_steps.append(steps[step_index])

                # Advance step index
                step_index += 1

                # Steps exhausted → terminal escalation
                if step_index >= len(steps):
                    escalation_available = True
                    escalated = True
                    started = False
                    current_step = None
                    step_index = len(steps)  # clamp to prevent runaway
                else:
                    started = True
                    current_step = steps[step_index]

            elif action == "resolved":
                product = request.form.get("product")
                problem = request.form.get("problem")
                description = request.form.get("description")
                step_index = int(request.form.get("step_index", 0))
                attempted_steps = request.form.getlist("attempted_steps")

                steps = KNOWLEDGE_BASE[product][problem]
                if 0 <= step_index < len(steps):
                    current_step = steps[step_index]
                    if not attempted_steps or attempted_steps[-1] != current_step:
                        attempted_steps.append(current_step)

                started = True
                current_state = "Resolved"

            elif action == "escalate":
                description = request.form.get("description")
                escalated = True
                started = False

        return render_template(
            "session.html",
            started=started,
            escalated=escalated,
            escalation_available=escalation_available,
            product=product,
            problem=problem,
            description=description,
            step_index=step_index,
            attempted_steps=attempted_steps,
            current_step=current_step,
            current_state=current_state
        )

    return app


if __name__ == "__main__":
    """
    Local development entry point.

    Debug is enabled for fast feedback during development.
    This will be turned off or configured differently later.
    """
    app = create_app()
    app.run(debug=True)
