from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.core.config import PRICING_MARGIN, RISK_THRESHOLD_HIGH, RISK_THRESHOLD_MEDIUM
from app.ml import ml_inference_service as ml
from app.models.transaction import TransactionType
from app.repositories.cash_snapshot import cash_snapshot_repository
from app.repositories.credit import credit_repository
from app.repositories.product import product_repository
from app.repositories.purchase import purchase_repository
from app.repositories.transaction import transaction_repository
from app.schemas.prediction import PriceRecommendationResponse, RiskScoreResponse


def get_product_trader_id(db: Session, product_id):
    product = product_repository.get(db, product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
        )
    return product.trader_id


def recommend_price(db: Session, product_id) -> PriceRecommendationResponse:
    history = purchase_repository.get_by_product(db, product_id)
    if not history:
        return PriceRecommendationResponse(
            product_id=product_id,
            predicted_replacement_cost=0.0,
            recommended_selling_price=0.0,
            note="Not enough purchase history yet — log a restock for this product to get a price recommendation.",
        )
    costs = [float(p.unit_cost_at_purchase) for p in history]
    predicted_cost = ml.predict_replacement_cost(costs)
    recommended_price = round(predicted_cost * (1 + PRICING_MARGIN), 2)
    return PriceRecommendationResponse(
        product_id=product_id,
        predicted_replacement_cost=round(predicted_cost, 2),
        recommended_selling_price=recommended_price,
        note=f"Price includes a {int(PRICING_MARGIN * 100)}% margin over the predicted next restocking cost.",
    )


def get_risk_score(db: Session, trader_id) -> RiskScoreResponse:
    transactions = transaction_repository.get_by_trader(db, trader_id)

    if not transactions:
        return RiskScoreResponse(
            trader_id=trader_id, risk_score=0.0, risk_label="unknown"
        )

    income = float(
        sum(t.amount for t in transactions if t.type == TransactionType.SALE)
    )
    expenses = float(
        sum(t.amount for t in transactions if t.type == TransactionType.EXPENSE)
    )
    withdrawals = float(
        sum(
            t.amount
            for t in transactions
            if t.type == TransactionType.PERSONAL_WITHDRAWAL
        )
    )
    open_credit = float(
        sum(
            c.amount_owed - c.amount_repaid
            for c in credit_repository.get_open_by_trader(db, trader_id)
        )
    )
    latest_snapshot = cash_snapshot_repository.get_latest_for_trader(db, trader_id)
    cash_on_hand = float(latest_snapshot.cash_on_hand) if latest_snapshot else 0.0

    score = ml.predict_risk_score(
        [income, expenses, withdrawals, open_credit, cash_on_hand]
    )
    label = (
        "high"
        if score >= RISK_THRESHOLD_HIGH
        else "medium"
        if score >= RISK_THRESHOLD_MEDIUM
        else "low"
    )
    return RiskScoreResponse(
        trader_id=trader_id, risk_score=round(score, 2), risk_label=label
    )
