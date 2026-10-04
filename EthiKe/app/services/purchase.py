from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.repositories.product import product_repository
from app.repositories.purchase import purchase_repository
from app.schemas.purchase import PurchaseCreate, PurchaseUpdate


def get_purchase(db: Session, purchase_id):
    purchase = purchase_repository.get(db, purchase_id)
    if not purchase:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Purchase not found"
        )
    return purchase


def get_purchase_history(db: Session, product_id):
    return purchase_repository.get_by_product(db, product_id)


def create_purchase(db: Session, data: PurchaseCreate, owned_trader_id):
    """Recording a purchase also restocks the product — keeps stock in sync automatically."""
    payload = data.model_dump()
    payload["trader_id"] = owned_trader_id
    purchase = purchase_repository.create(db, payload)
    product = product_repository.get(db, data.product_id)
    if product:
        product.current_stock_quantity += data.quantity
        db.commit()
    return purchase


def update_purchase(db: Session, purchase_id, data: PurchaseUpdate):
    """Partial update — if quantity changes, adjusts stock by the delta so it stays accurate."""
    purchase = get_purchase(db, purchase_id)
    updates = data.model_dump(exclude_unset=True)
    if "quantity" in updates:
        product = product_repository.get(db, purchase.product_id)
        if product:
            product.current_stock_quantity += updates["quantity"] - purchase.quantity
    return purchase_repository.update(db, purchase, updates)


def delete_purchase(db: Session, purchase_id):
    """Deleting a purchase reverses its effect on stock."""
    purchase = get_purchase(db, purchase_id)
    product = product_repository.get(db, purchase.product_id)
    if product:
        product.current_stock_quantity -= purchase.quantity
        db.commit()
    purchase_repository.delete(db, purchase)
