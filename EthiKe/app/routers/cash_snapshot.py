from fastapi import APIRouter, Depends, status
from uuid import UUID
from sqlalchemy.orm import Session
from database import get_db
from dependencies import get_current_user, require_roles, assert_can_access_trader, get_owned_trader_id
from app.models.user import User, UserRole
from app.schemas.cash_snapshot import CashSnapshotCreate, CashSnapshotUpdate, CashSnapshotRead
from app.services import cash_snapshot as cash_snapshot_service

router = APIRouter(prefix="/cash-snapshots", tags=["CashSnapshot"], dependencies=[Depends(get_current_user)])
ADMIN_ONLY = Depends(require_roles(UserRole.ADMIN))


@router.get("/", response_model=list[CashSnapshotRead], dependencies=[ADMIN_ONLY])
def list_snapshots(db: Session = Depends(get_db)):
    """Admin only — traders use GET /trader/{trader_id}/latest for their own."""
    return cash_snapshot_service.list_snapshots(db)


@router.get("/trader/{trader_id}/latest", response_model=CashSnapshotRead)
def get_latest_snapshot(trader_id: UUID, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    assert_can_access_trader(trader_id, current_user)
    return cash_snapshot_service.get_latest_snapshot(db, trader_id)


@router.get("/{cash_snapshot_id}", response_model=CashSnapshotRead)
def get_snapshot(cash_snapshot_id: UUID, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    snapshot = cash_snapshot_service.get_snapshot(db, cash_snapshot_id)
    assert_can_access_trader(snapshot.trader_id, current_user)
    return snapshot


@router.post("/trader/{trader_id}/compute", response_model=CashSnapshotRead)
def compute_snapshot(trader_id: UUID, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    assert_can_access_trader(trader_id, current_user)
    return cash_snapshot_service.compute_snapshot(db, trader_id)


@router.post("/", response_model=CashSnapshotRead, status_code=status.HTTP_201_CREATED)
def create_snapshot(data: CashSnapshotCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    owned_trader_id = get_owned_trader_id(data.trader_id, current_user)
    return cash_snapshot_service.create_snapshot(db, data, owned_trader_id)


@router.put("/{cash_snapshot_id}", response_model=CashSnapshotRead)
def replace_snapshot(cash_snapshot_id: UUID, data: CashSnapshotCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    snapshot = cash_snapshot_service.get_snapshot(db, cash_snapshot_id)
    assert_can_access_trader(snapshot.trader_id, current_user)
    owned_trader_id = get_owned_trader_id(data.trader_id, current_user)
    return cash_snapshot_service.replace_snapshot(db, cash_snapshot_id, data, owned_trader_id)


@router.patch("/{cash_snapshot_id}", response_model=CashSnapshotRead)
def update_snapshot(cash_snapshot_id: UUID, data: CashSnapshotUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    snapshot = cash_snapshot_service.get_snapshot(db, cash_snapshot_id)
    assert_can_access_trader(snapshot.trader_id, current_user)
    return cash_snapshot_service.update_snapshot(db, cash_snapshot_id, data)


@router.delete("/{cash_snapshot_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_snapshot(cash_snapshot_id: UUID, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    snapshot = cash_snapshot_service.get_snapshot(db, cash_snapshot_id)
    assert_can_access_trader(snapshot.trader_id, current_user)
    cash_snapshot_service.delete_snapshot(db, cash_snapshot_id)
