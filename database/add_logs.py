from fastapi import Depends
from .schema import Activity_Logs
from .db import get_db
from sqlalchemy.orm import Session


def add_log(user_id:str,log_name:str,description:str,db: Session):
    db_logs = Activity_Logs(user_id=user_id,log_name=log_name,description=description)
    db.add(db_logs)
    db.commit()
    db.refresh(db_logs)