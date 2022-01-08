from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Numeric

from .config import DB_URL

Base = declarative_base()


class DataVector(Base):
    __tablename__ = "vectors"

    vectors_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer)
    datatype_x = Column(String(30))
    datatype_y = Column(String(30))
    by_date_computed = Column(DateTime)
    correlation_value = Column(Numeric)
    p_value = Column(Numeric)


if __name__ == "__main__":
    engine = create_engine(DB_URL)
    Base.metadata.create_all(engine)
