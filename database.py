from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import uuid

Base = declarative_base()
engine = create_engine('sqlite:///maze_runner.db', echo=False)
SessionLocal = sessionmaker(bind=engine)

class SimulationResult(Base):
    __tablename__ = 'simulations'
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    timestamp = Column(DateTime, default=datetime.utcnow)
    scenario_type = Column(String) # 'European Call', 'Pi Estimation'
    n_samples = Column(Integer)
    true_value = Column(Float)
    estimated_value = Column(Float)
    error = Column(Float)
    method = Column(String) # 'Standard', 'Antithetic'
    computation_time = Column(Float)

Base.metadata.create_all(engine)

def save_result(scenario, n_samples, true_val, est_val, method, time_taken):
    session = SessionLocal()
    result = SimulationResult(
        scenario_type=scenario,
        n_samples=n_samples,
        true_value=true_val,
        estimated_value=est_val,
        error=abs(true_val - est_val),
        method=method,
        computation_time=time_taken
    )
    session.add(result)
    session.commit()
    session.close()