from fastapi import APIRouter, HTTPException
from app.models.audit import StartAuditResponse, QuestionResponse, AnswerRequest
from app.services.audit_engine import AuditEngine

router = APIRouter(prefix="/audit", tags=["audit"])

@router.post("/start", response_model=StartAuditResponse)
async def start_audit():
    """
    Initialize a new audit session and return its ID.
    """
    session_id = await AuditEngine.create_session()
    return StartAuditResponse(session_id=session_id)

@router.get("/{session_id}/next", response_model=QuestionResponse)
async def get_next_question(session_id: str):
    """
    Retrieve the next ISO 27001 clause question for this session.
    """
    try:
        question = await AuditEngine.next_question(session_id)
    except KeyError:
        raise HTTPException(status_code=404, detail="Session not found")
    return QuestionResponse(question=question)

@router.post("/{session_id}/answer", status_code=204)
async def post_answer(session_id: str, req: AnswerRequest):
    """
    Record the user’s answer and advance to the next clause.
    """
    try:
        await AuditEngine.record_answer(session_id, req.answer)
    except KeyError:
        raise HTTPException(status_code=404, detail="Session not found")