from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.integrations.openai_client import OpenAIServiceError
from app.schemas import SpendingAnalysis
from app.services import ai_service


router = APIRouter(
    prefix="/ai",
    tags=["AI"]
)


@router.get(
    "/spending-analysis/{user_id}",
    response_model=SpendingAnalysis
)
def get_spending_analysis(
    user_id: int,
    db: Session = Depends(get_db)
):
    try:
        analysis = ai_service.analyze_spending(
            db=db,
            user_id=user_id
        )
    except OpenAIServiceError:
        raise HTTPException(
            status_code=503,
            detail="AI service is temporarily unavailable"
        )

    if analysis == "user_not_found":
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    if analysis is None:
        raise HTTPException(
            status_code=404,
            detail="No transactions found for this user"
        )

    return analysis