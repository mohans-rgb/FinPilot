from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from .settings import settings

engine = create_engine(settings.DATABASE_URL, echo=False)
LocalSession = sessionmaker(bind=engine)

class Base(DeclarativeBase):
    pass

def init_db():
    from . import models
    Base.metadata.create_all(engine)
