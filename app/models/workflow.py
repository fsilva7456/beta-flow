from sqlalchemy import Column, Integer, String, DateTime, JSON, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class Workflow(Base):
    __tablename__ = "workflows"

    id = Column(Integer, primary_key=True, index=True)
    workflow_name = Column(String, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    steps = relationship("WorkflowStep", back_populates="workflow")

class WorkflowStep(Base):
    __tablename__ = "workflow_steps"

    id = Column(Integer, primary_key=True, index=True)
    workflow_id = Column(Integer, ForeignKey("workflows.id"))
    step_name = Column(String)
    action = Column(String)
    parameters = Column(JSON)
    condition = Column(JSON)
    group = Column(String, nullable=True)
    order = Column(Integer)
    workflow = relationship("Workflow", back_populates="steps")
