from pydantic import BaseModel

class StartAuditResponse(BaseModel):
    session_id: str

class QuestionResponse(BaseModel):
    question: str

class AnswerRequest(BaseModel):
    answer: str
