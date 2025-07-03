import uuid
from datetime import datetime
from app.services.mongo_client import db

# Your list of clause questions
CLAUSES = [
    "Clause 4.1: What is the scope of the ISMS?",
    "Clause 4.2: What are the internal and external issues?",
    "Clause 5.1: How is leadership demonstrating commitment?",
    "Clause 5.2: What is the ISMS policy?",
    "Clause 6.1: What are the risk assessment and treatment processes?",
    "Clause 6.2: What are the information security objectives?",
    "Clause 7.1: What resources are needed for the ISMS?",
    "Clause 7.2: How is competence ensured?",
    "Clause 7.3: How is awareness raised among employees?",
    "Clause 7.4: How is communication managed?",
    "Clause 7.5: How is documented information controlled?",
    "Clause 8.1: How are operations planned and controlled?",
    "Clause 8.2: How are risks and opportunities addressed?",
    "Clause 9.1: How is performance evaluated?",
    "Clause 9.2: How is internal audit conducted?",
    # …etc.
]

class AuditEngine:
    @staticmethod
    async def create_session() -> str:
        session_id = str(uuid.uuid4())
        await db.sessions.insert_one({
            "_id": session_id,
            "clause_index": 0
        })
        return session_id

    @staticmethod
    async def next_question(session_id: str) -> str:
        sess = await db.sessions.find_one({"_id": session_id})
        if not sess:
            raise KeyError("Session not found")
        idx = sess["clause_index"]
        if idx >= len(CLAUSES):
            return "🔔 Audit complete! No more questions."
        return CLAUSES[idx]

    @staticmethod
    async def record_answer(session_id: str, answer: str):
        # 1) Fetch the session and current clause index
        sess = await db.sessions.find_one({"_id": session_id})
        if not sess:
            raise KeyError("Session not found")
        idx = sess["clause_index"]
        if idx >= len(CLAUSES):
            raise IndexError("No more clauses to answer")

        # 2) Get the question text
        clause_text = CLAUSES[idx]

        # 3) Insert a response document
        await db.responses.insert_one({
            "session_id": session_id,
            "clause_index": idx,
            "clause": clause_text,
            "answer": answer,
            "answered_at": datetime.utcnow()
        })

        # 4) Advance to the next clause
        await db.sessions.update_one(
            {"_id": session_id},
            {"$inc": {"clause_index": 1}}
        )
