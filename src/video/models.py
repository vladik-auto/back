from datetime import datetime

from src.database import Base
from typing import Annotated
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from sqlalchemy.sql import expression
from sqlalchemy.types import DateTime
from sqlalchemy.ext.compiler import compiles


class utcnow(expression.FunctionElement):
    type = DateTime()
    inherit_cache = True


@compiles(utcnow, "postgresql")
def pg_utcnow(element, compiler, **kw):
    return "TIMEZONE('utc', CURRENT_TIMESTAMP)"


pk_id = Annotated[int, mapped_column(primary_key=True, autoincrement=True)]
created_at = Annotated[datetime, mapped_column(server_default=utcnow(), default=utcnow())]
updated_at = Annotated[datetime, mapped_column(default=utcnow(), server_default=utcnow(), onupdate=utcnow())]


class AttributeMixin:
    id: Mapped[pk_id]
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]


class Video(Base, AttributeMixin):
    __tablename__ = "video"
    employee_id: Mapped[int] = mapped_column(ForeignKey("employee.id"))
    title: Mapped[str]
    description: Mapped[str]


class VideoViolations(Base):
    __tablename__ = "video_violation"
    video_id: Mapped[int] = mapped_column(ForeignKey("video.id"), primary_key=True)
    violation_id: Mapped[int] = mapped_column(ForeignKey("violation.id"), primary_key=True)
    is_spectated: Mapped[bool] = mapped_column(default=False)
    created_at = created_at


class Violations(Base, AttributeMixin):
    __tablename__ = "violation"

    name: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str]


class Employee(Base, AttributeMixin):
    __tablename__ = "employee"
    first_name: Mapped[str] = mapped_column(nullable=False)
    middle_name: Mapped[str] = mapped_column(nullable=False)
    last_name: Mapped[str] = mapped_column(nullable=False)
    class Config:
        from_attributes = True


class EmployeeViolations(Base, AttributeMixin):
    __tablename__ = "employee_violation"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    violation_id: Mapped[int] = mapped_column(ForeignKey("violation.id"))
    employee_id: Mapped[int] = mapped_column(ForeignKey("employee.id"))
    created_at = created_at
