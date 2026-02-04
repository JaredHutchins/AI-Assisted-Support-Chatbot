"""
Minimal Flask entry point for the AI-Assisted Support Chatbot (ASC).

This file exists to prove:
- the environment is set up correctly
- Flask runs without errors
- we have a clean baseline to build on

Nothing fancy here. This is intentional.
"""


from flask import Flask, render_template, request
from app.flows.product_troubleshooting_flow import ProductTroubleshootingFlow
from app.knowledge_base import load_knowledge_base
from app.routes.session_routes import session_routes
from app.session_context import SessionContext

KNOWLEDGE_BASE = load_knowledge_base()

# Reasoning component aligned with UML flow structure.
FLOW_ENGINE = ProductTroubleshootingFlow(KNOWLEDGE_BASE)


def build_product_problem_map(knowledge_base: dict) -> dict:
    """
    Build a simple map the template can use for product/problem dropdowns.
    """
    # One source of truth keeps the form options in sync with the knowledge file.
    return {
        product_name: list(problem_map.keys())
        for product_name, problem_map in knowledge_base.items()
        if isinstance(problem_map, dict)
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
        product_problem_map = build_product_problem_map(KNOWLEDGE_BASE)

        def parse_step_index(raw_value: str) -> int:
            # Hidden form values can still be tampered with; fail safe to 0.
            try:
                return max(0, int(raw_value))
            except (TypeError, ValueError):
                return 0

        def get_steps(selected_product: str, selected_problem: str) -> list:
            return FLOW_ENGINE.retrieveArticle(selected_product, selected_problem)

        if request.method == "POST":
            action = request.form.get("action")

            # Initial session start
            if action == "start":
                product = request.form.get("product")
                problem = request.form.get("problem")
                description = request.form.get("description")
                steps = get_steps(product, problem)
                ctx = SessionContext("ui-session")

                if steps and ctx.startSession(product, problem, len(steps)):
                    started = True
                    step_index = ctx.currentStepIndex
                    attempted_steps = list(ctx.attemptedSteps)
                    current_step = FLOW_ENGINE.getNextStep(product, problem, step_index)
                    current_state = ctx.currentState

            # Troubleshooting loop
            elif action == "not_resolved":
                product = request.form.get("product")
                problem = request.form.get("problem")
                description = request.form.get("description")
                step_index = parse_step_index(request.form.get("step_index"))
                attempted_steps = request.form.getlist("attempted_steps")
                steps = get_steps(product, problem)
                ctx = SessionContext("ui-session")

                if steps and ctx.restoreKnowledgeRetrieval(
                    product=product,
                    problem=problem,
                    attemptedSteps=attempted_steps,
                    stepIndex=step_index,
                    maxSteps=len(steps)
                ):
                    current_step = FLOW_ENGINE.getNextStep(product, problem, ctx.currentStepIndex)

                    escalated_now = ctx.continueTroubleshooting(current_step)
                    attempted_steps = list(ctx.attemptedSteps)
                    step_index = ctx.currentStepIndex

                    if escalated_now or step_index >= len(steps):
                        escalation_available = True
                        escalated = True
                        started = False
                        current_state = "Escalated"
                        current_step = None
                    else:
                        started = True
                        current_state = ctx.currentState
                        current_step = FLOW_ENGINE.getNextStep(product, problem, step_index)

            elif action == "resolved":
                product = request.form.get("product")
                problem = request.form.get("problem")
                description = request.form.get("description")
                step_index = parse_step_index(request.form.get("step_index"))
                attempted_steps = request.form.getlist("attempted_steps")
                steps = get_steps(product, problem)
                ctx = SessionContext("ui-session")

                if steps and ctx.restoreKnowledgeRetrieval(
                    product=product,
                    problem=problem,
                    attemptedSteps=attempted_steps,
                    stepIndex=step_index,
                    maxSteps=len(steps)
                ):
                    current_step = FLOW_ENGINE.getNextStep(product, problem, ctx.currentStepIndex)
                    if current_step and ctx.resolveTroubleshooting(current_step):
                        attempted_steps = list(ctx.attemptedSteps)
                        step_index = ctx.currentStepIndex
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
            current_state=current_state,
            product_problem_map=product_problem_map,
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
