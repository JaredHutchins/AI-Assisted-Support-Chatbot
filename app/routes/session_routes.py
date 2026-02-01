

"""
ASC Session Routes

Thin HTTP orchestration layer only.
- Defines API endpoints and URL structure
- Parses request JSON and returns response JSON
- Delegates all behavior to the existing session engine
- Performs no business logic and no state management
"""

from flask import Blueprint, request, jsonify

# Session engine (authoritative logic)
# NOTE: Import path must match existing engine module
from app.session_context import SessionContext

session_routes = Blueprint("session_routes", __name__, url_prefix="/api/session")


@session_routes.route("/start", methods=["POST"])
def start_session():
    """
    Start a new support session.

    State transition:
        Idle -> Issue Capture -> Knowledge Retrieval

    Expected JSON:
        sessionId (str)
        product (str)
        issueDescription (str)
    """
    data = request.get_json(force=True)

    # Delegate to session engine (implementation handled there)
    result = SessionContext.start_session(
        session_id=data.get("sessionId"),
        product=data.get("product"),
        issue_description=data.get("issueDescription"),
    )

    return jsonify(result), 200


@session_routes.route("/step", methods=["POST"])
def submit_step():
    """
    Submit the outcome of a troubleshooting step.

    State transition:
        Knowledge Retrieval ->
            Knowledge Retrieval | Resolved | Escalated

    Expected JSON:
        sessionId (str)
        stepId (str)
        outcome (str)
    """
    data = request.get_json(force=True)

    result = SessionContext.submit_step(
        session_id=data.get("sessionId"),
        step_id=data.get("stepId"),
        outcome=data.get("outcome"),
    )

    return jsonify(result), 200


@session_routes.route("/escalate", methods=["POST"])
def escalate_session():
    """
    Escalate the current session.

    State transition:
        Knowledge Retrieval -> Escalation -> Session Complete

    Expected JSON:
        sessionId (str)
        reason (str)
    """
    data = request.get_json(force=True)

    result = SessionContext.escalate(
        session_id=data.get("sessionId"),
        reason=data.get("reason"),
    )

    return jsonify(result), 200


@session_routes.route("/status", methods=["GET"])
def get_status():
    """
    Retrieve current session status.

    Read-only endpoint.
    No state transitions.

    Query params:
        sessionId (str)
    """
    session_id = request.args.get("sessionId")

    result = SessionContext.get_status(session_id=session_id)

    return jsonify(result), 200