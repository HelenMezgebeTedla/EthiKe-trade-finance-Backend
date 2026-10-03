from fastapi import APIRouter, Depends, status
from uuid import UUID
from sqlalchemy.orm import Session
from database import get_db
from dependencies import get_current_user, assert_can_access_trader
from app.models.user import User
from app.schemas.sale import SaleCreate, SaleUpdate, SaleRead
from app.services import sale as sale_service

router = APIRouter(prefix="/sales", tags=["Sale"], dependencies=[Depends(get_current_user)])


@router.get("/product/{product_id}", response_model=list[SaleRead])
def list_product_sales(product_id: UUID, db: Session = Depends(get_db)):
    return sale_service.list_product_sales(db, product_id)


@router.get("/{sale_id}", response_model=SaleRead)
def get_sale(sale_id: UUID, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    sale = sale_service.get_sale(db, sale_id)
    assert_can_access_trader(sale_service.get_sale_trader_id(db, sale), current_user)
    return sale


@router.post("/", response_model=SaleRead, status_code=status.HTTP_201_CREATED)
def create_sale(data: SaleCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    assert_can_access_trader(sale_service.get_transaction_trader_id(db, data.transaction_id), current_user)
    return sale_service.create_sale(db, data)


@router.put("/{sale_id}", response_model=SaleRead)
def replace_sale(sale_id: UUID, data: SaleUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    sale = sale_service.get_sale(db, sale_id)
    assert_can_access_trader(sale_service.get_sale_trader_id(db, sale), current_user)
    return sale_service.update_sale(db, sale_id, data)


@router.patch("/{sale_id}", response_model=SaleRead)
def update_sale(sale_id: UUID, data: SaleUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    sale = sale_service.get_sale(db, sale_id)
    assert_can_access_trader(sale_service.get_sale_trader_id(db, sale), current_user)
    return sale_service.update_sale(db, sale_id, data)


@router.delete("/{sale_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_sale(sale_id: UUID, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    sale = sale_service.get_sale(db, sale_id)
    assert_can_access_trader(sale_service.get_sale_trader_id(db, sale), current_user)
    sale_service.delete_sale(db, sale_id)
