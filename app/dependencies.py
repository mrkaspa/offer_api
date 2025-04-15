from typing import Annotated
from fastapi import Depends
from sqlalchemy.orm import Session
from app.persistance import connect_to_db, get_session

engine = connect_to_db()
SessionDep = Annotated[Session, Depends(get_session(engine))]
