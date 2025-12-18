from sqlalchemy import Column, Integer, String, Boolean, DateTime
from datetime import datetime
import pytz
from database import Base

def wib_now():
    return datetime.now(pytz.timezone("Asia/Jakarta"))

class TriageLog(Base):
    __tablename__ = "triage_logs"

    id = Column(Integer, primary_key=True, index=True)
    age = Column(Integer)
    complaint = Column(String)
    triage_result = Column(String)
    danger_sign = Column(Boolean)
    risk_group = Column(Boolean)
    created_at = Column(DateTime, default=wib_now)

