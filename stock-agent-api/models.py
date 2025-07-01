from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Boolean
from sqlalchemy.orm import declarative_base, sessionmaker

engine = create_engine("sqlite:///alerts.db", echo=False, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False)
Base = declarative_base()

class PriceAlert(Base):
    __tablename__ = "price_alerts"

    id          = Column(Integer, primary_key=True, index=True)
    symbol      = Column(String, index=True, nullable=False)
    direction   = Column(String, nullable=False)  # 'above' / 'below'
    price       = Column(Float,  nullable=False)
    created_at  = Column(DateTime, default=datetime.utcnow)
    triggered   = Column(Boolean, default=False)

def init_db():
    Base.metadata.create_all(bind=engine)
