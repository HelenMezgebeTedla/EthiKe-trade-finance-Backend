from fastapi import APIRouter, Depends
from uuid import UUID
from sqlalchemy.orm import Session
from database import get_db
from dependencies import get_current_user, assert_can_access_trader
from app.models.user import User
from app.schemas.prediction import PriceRecommendationResponse, RiskScoreResponse
from app.services import prediction as prediction_service

router = APIRouter(prefix="/predictions", tags=["Prediction"], dependencies=[Depends(get_current_user)])


@router.get("/price-recommendation/{product_id}", response_model=PriceRecommendationResponse)
def get_price_recommendation(product_id: UUID, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    owner_trader_id = prediction_service.get_product_trader_id(db, product_id)
    assert_can_access_trader(owner_trader_id, current_user)
    return prediction_service.recommend_price(db, product_id)


@router.get("/risk-score/{trader_id}", response_model=RiskScoreResponse)
def get_risk_score(trader_id: UUID, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    assert_can_access_trader(trader_id, current_user)
    return prediction_service.get_risk_score(db, trader_id)
