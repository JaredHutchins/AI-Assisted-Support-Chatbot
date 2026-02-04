"""
ASC Session Routes

Thin HTTP orchestration layer only.
- Defines API endpoints and URL structure
- Parses request JSON and returns response JSON
- Delegates all behavior to the existing session engine
- Performs no business logic and no state management
"""

from flask import Blueprint, request, jsonify

from app.knowledge_base import get_max_steps
# Session engine (authoritative logic)
# NOTE: Import path must match existing engine module
from app.session_context import SessionContext

# In-memory session registry (demo scope only)
SESSIONS = {}

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

    session_id = data.get("sessionId")
    product = data.get("product")
    issue_description = data.get("issueDescription")
    requested_max_steps = data.get("maxSteps")

    if not session_id or not product or not issue_description:
        return jsonify({"error": "sessionId, product, and issueDescription are required"}), 400

    if requested_max_steps is None:
        max_steps = get_max_steps(product, issue_description, default=3)
    else:
        try:
            max_steps = max(1, int(requested_max_steps))
        except (TypeError, ValueError):
            return jsonify({"error": "maxSteps must be a positive integer"}), 400

    ctx = SessionContext(session_id)
    initialized = ctx.startSession(product, issue_description, max_steps)
    if not initialized:
        return jsonify({"error": "failed to initialize session state"}), 500

    SESSIONS[session_id] = ctx

    return jsonify({
        "sessionId": session_id,
        "currentState": ctx.currentState,
        "terminal": ctx.isTerminal()
    }), 200


@session_routes.route("/step", methods=["POST"])
def submit_step():
    data = request.get_json(force=True)

    session_id = data.get("sessionId")
    step = data.get("step")
    resolved = data.get("resolved")

    if not session_id or session_id not in SESSIONS:
        return jsonify({"error": "invalid sessionId"}), 400

    ctx = SESSIONS[session_id]

    # If resolved, mark and stop
    if resolved is True:
        if not ctx.markResolved():
            return jsonify({"error": "invalid state transition for resolution"}), 400
        return jsonify({
            "sessionId": ctx.sessionId,
            "currentState": ctx.currentState,
            "terminal": ctx.isTerminal()
        }), 200

    # Not resolved: delegate progression and escalation decision to session logic
    escalated_now = ctx.continueTroubleshooting(step)
    if escalated_now:
        return jsonify(ctx.getSummary()), 200

    # Otherwise continue troubleshooting
    return jsonify({
        "sessionId": ctx.sessionId,
        "currentState": ctx.currentState,
        "stepIndex": ctx.currentStepIndex,
        "terminal": ctx.isTerminal()
    }), 200


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

    session_id = data.get("sessionId")
    if not session_id or session_id not in SESSIONS:
        return jsonify({"error": "invalid sessionId"}), 400

    ctx = SESSIONS[session_id]
    if not ctx.markEscalated():
        return jsonify({"error": "invalid state transition for escalation"}), 400

    return jsonify(ctx.getSummary()), 200


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
    if not session_id:
        return jsonify({"error": "sessionId is required"}), 400

    return jsonify({
        "sessionId": session_id,
        "status": "unknown",
        "terminal": False
    }), 200
