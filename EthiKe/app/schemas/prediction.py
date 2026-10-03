from uuid import UUID
from pydantic import BaseModel


class PriceRecommendationResponse(BaseModel):
    product_id: UUID
    predicted_replacement_cost: float
    recommended_selling_price: float
    note: str


class RiskScoreResponse(BaseModel):
    trader_id: UUID
    risk_score: float
    risk_label: str
