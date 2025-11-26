# app/models/task.py
from sqlalchemy import (
    Column, Integer, String, Text, JSON, ForeignKey, DateTime,
    Enum, SmallInteger, func
)
from sqlalchemy.orm import relationship
from app.database import Base
from typing import Literal
import enum


# Task status enum (matches frontend expectations)
class TaskStatus(str, enum.Enum):
    pending = "pending"
    running = "running"
    completed = "completed"
    failed = "failed"
    cancelled = "cancelled"


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False, default="Untitled Scraping Task")
    task_type = Column(String, index=True, nullable=False)  # e.g. "amazon_price", "linkedin_profile"
    url = Column(Text, nullable=False)
    parameters = Column(JSON, default=dict)  # Extra params (selectors, pagination, etc.)

    status = Column(Enum(TaskStatus), default=TaskStatus.pending, nullable=False, index=True)
    progress = Column(SmallInteger, default=0)  # 0–100
    result = Column(JSON, nullable=True)       # Final scraped data
    logs = Column(Text, default="")            # Accumulated logs (or use separate table for big logs)
    error_message = Column(Text, nullable=True)

    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)
    started_at = Column(DateTime(timezone=True), nullable=True)
    finished_at = Column(DateTime(timezone=True), nullable=True)

    # Foreign Key
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)

    # Relationships
    owner = relationship("User", back_populates="tasks")

    def to_dict(self):
        """Convenient for WebSocket broadcasts"""
        return {
            "id": self.id,
            "title": self.title,
            "task_type": self.task_type,
            "url": self.url,
            "status": self.status.value,
            "progress": self.progress,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "finished_at": self.finished_at.isoformat() if self.finished_at else None,
            "has_result": self.result is not None,
            "error": self.error_message,
        }

    def __repr__(self) -> str:
        return f"<Task {self.id} [{self.status.value}] {self.title[:30]}...>"