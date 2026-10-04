from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.repositories.product import product_repository
from app.repositories.sale import sale_repository
from app.repositories.transaction import transaction_repository
from app.schemas.sale import SaleCreate, SaleUpdate


def get_sale(db: Session, sale_id):
    sale = sale_repository.get(db, sale_id)
    if not sale:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Sale not found"
        )
    return sale


def get_sale_trader_id(db: Session, sale):
    """Sale has no trader_id column — ownership is resolved through its linked Transaction."""
    transaction = transaction_repository.get(db, sale.transaction_id)
    return transaction.trader_id if transaction else None


def get_transaction_trader_id(db: Session, transaction_id):
    transaction = transaction_repository.get(db, transaction_id)
    if not transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Transaction not found"
        )
    return transaction.trader_id


def list_product_sales(db: Session, product_id):
    return sale_repository.get_by_product(db, product_id)


def create_sale(db: Session, data: SaleCreate):
    """Recording a sale also reduces stock — keeps stock in sync automatically."""
    sale = sale_repository.create(db, data.model_dump())
    product = product_repository.get(db, data.product_id)
    if product:
        product.current_stock_quantity -= data.quantity_sold
        db.commit()
    return sale


def update_sale(db: Session, sale_id, data: SaleUpdate):
    """If quantity_sold changes, adjusts stock by the delta so it stays accurate."""
    sale = get_sale(db, sale_id)
    updates = data.model_dump(exclude_unset=True)
    if "quantity_sold" in updates:
        product = product_repository.get(db, sale.product_id)
        if product:
            product.current_stock_quantity -= (
                updates["quantity_sold"] - sale.quantity_sold
            )
    return sale_repository.update(db, sale, updates)


def delete_sale(db: Session, sale_id):
    """Deleting a sale reverses its effect on stock."""
    sale = get_sale(db, sale_id)
    product = product_repository.get(db, sale.product_id)
    if product:
        product.current_stock_quantity += sale.quantity_sold
        db.commit()
    sale_repository.delete(db, sale)
