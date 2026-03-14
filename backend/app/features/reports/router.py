from datetime import datetime
from fastapi import APIRouter, Depends, Query
from sqlmodel import Session

from app.core.security import get_current_org_id, get_current_user_id
from app.database.session import get_session
from app.features.reports.service import build_agency_report
from app.features.trips.permissions import ensure_org_member
from app.schemas.report import AgencyReport


router = APIRouter(prefix="/reports", tags=["Reports"])


@router.get("/agency", response_model=AgencyReport)
def agency_report_endpoint(
    start: datetime | None = Query(default=None),
    end: datetime | None = Query(default=None),
    session: Session = Depends(get_session),
    user_id: int = Depends(get_current_user_id),
    org_id: int = Depends(get_current_org_id),
):
    ensure_org_member(session, org_id, user_id)
    return build_agency_report(session, org_id, start, end)
