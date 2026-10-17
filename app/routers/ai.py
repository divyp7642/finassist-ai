
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import get_current_user_id
from app.integrations.openai_client import OpenAIServiceError
from app.schemas import SpendingAnalysis
from app.services import ai_service


router = APIRouter(
    prefix="/ai",
    tags=["AI"]
)


# GET AI SPENDING ANALYSIS
@router.get(
    "/spending-analysis/{user_id}",
    response_model=SpendingAnalysis
)
def get_spending_analysis(
    user_id: int,
    db: Session = Depends(get_db),
    current_user_id: int = Depends(get_current_user_id)
):
    # Step 1: Verify user ownership
    if user_id != current_user_id:
        raise HTTPException(
            status_code=403,
            detail="You cannot access another user's spending analysis"
        )

    # Step 2: Generate spending analysis
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

    # Step 3: Check whether user exists
    if analysis == "user_not_found":
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    # Step 4: Check whether transactions exist
    if analysis is None:
        raise HTTPException(
            status_code=404,
            detail="No transactions found for this user"
        )

    # Step 5: Return AI-generated analysis
    return analysis
