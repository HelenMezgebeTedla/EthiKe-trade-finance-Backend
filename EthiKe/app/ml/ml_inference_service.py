import os

import joblib
import pandas as pd

_MODEL_DIR = os.path.dirname(__file__)
_replacement_cost_model = None
_risk_classifier_model = None


def _load_models():
    global _replacement_cost_model, _risk_classifier_model
    rc_path = os.path.join(_MODEL_DIR, "replacement_cost_model.pkl")
    risk_path = os.path.join(_MODEL_DIR, "risk_classifier_model.pkl")
    if os.path.exists(rc_path):
        _replacement_cost_model = joblib.load(rc_path)
    if os.path.exists(risk_path):
        _risk_classifier_model = joblib.load(risk_path)


_load_models()

N_LAG = 5


def _build_lag_features(recent_purchase_costs: list) -> list:
    if not recent_purchase_costs:
        return [0.0] * N_LAG
    costs = [float(c) for c in recent_purchase_costs][-N_LAG:]
    if len(costs) < N_LAG:
        costs = [costs[0]] * (N_LAG - len(costs)) + costs
    return costs


def predict_replacement_cost(recent_purchase_costs: list) -> float:
    features = _build_lag_features(recent_purchase_costs)
    if _replacement_cost_model is not None:
        df = pd.DataFrame([features], columns=[f"lag_{i + 1}" for i in range(N_LAG)])
        return float(_replacement_cost_model.predict(df)[0])
    if not recent_purchase_costs:
        return 0.0
    return float(recent_purchase_costs[-1]) * 1.03


def predict_risk_score(trader_features: list) -> float:
    if _risk_classifier_model is not None:
        df = pd.DataFrame(
            [trader_features],
            columns=[
                "income",
                "expenses",
                "withdrawals",
                "open_credit",
                "cash_on_hand",
            ],
        )
        return float(_risk_classifier_model.predict_proba(df)[0][1])
    if not trader_features or len(trader_features) < 3:
        return 0.5
    income, expenses, withdrawals = (
        trader_features[0],
        trader_features[1],
        trader_features[2],
    )
    if income <= 0:
        return 0.9
    return min(1.0, max(0.0, float(expenses + withdrawals) / float(income) - 0.5))
