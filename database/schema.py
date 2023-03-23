from sqlalchemy import Boolean, Column, ForeignKey, Integer, String,DateTime,func
from sqlalchemy.orm import relationship

from .db import Base

class Activity_Logs(Base):
    __tablename__ = "activity_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String)
    log_name = Column(String)
    description = Column(String)
    created_at = Column(DateTime, default=func.now(), nullable=False)
