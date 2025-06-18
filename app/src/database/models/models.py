import enum
from datetime import date, datetime
from typing import Optional, Set

from sqlalchemy import DateTime, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, unique=True)

    first_name: Mapped[Optional[str]]
    last_name: Mapped[Optional[str]]
    login: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    employments: Mapped[Set["Company"]] = relationship(
        secondary="companies_to_users", back_populates="employees"
    )

    expenses: Mapped[Set["Expense"]] = relationship(back_populates="driver")


class Role(Base):
    __tablename__ = "roles"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, unique=True)

    # Data control
    can_view_data: Mapped[bool]
    can_edit_vehicles: Mapped[bool]
    can_edit_employees: Mapped[bool]
    can_edit_expense_categories: Mapped[bool]

    # Integrations and data sourses
    can_view_data_sourses: Mapped[bool]
    can_create_data_sourses: Mapped[bool]
    can_import_from_files: Mapped[bool]
    can_edit_sync_settings: Mapped[bool]

    # Finansial ops
    can_create_expenses: Mapped[bool]
    can_approve_expenses: Mapped[bool]
    can_correct_expense_amounts: Mapped[bool]
    can_remove_expenses: Mapped[bool]

    # Moderation
    can_add_employees: Mapped[bool]
    can_create_roles: Mapped[bool]
    can_assign_roles: Mapped[bool]
    can_edit_roles: Mapped[bool]

    id_company: Mapped[int] = mapped_column(ForeignKey("companies.id"))
    company: Mapped["Company"] = relationship(back_populates="roles")


class Company(Base):
    __tablename__ = "companies"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, unique=True)

    name: Mapped[str] = mapped_column(nullable=False)
    employees: Mapped[Set[User]] = relationship(
        secondary="companies_to_users", back_populates="employments"
    )

    roles: Mapped[Set[Role]] = relationship(back_populates="company")
    vehicles: Mapped[Set["Vehicle"]] = relationship(back_populates="company")
    expenses: Mapped[Set["Expense"]] = relationship(back_populates="company")


class Employment(Base):
    __tablename__ = "companies_to_users"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, unique=True)

    created_at: Mapped[datetime] = mapped_column(default=func.now())

    id_user: Mapped[int] = mapped_column(ForeignKey("users.id"))
    id_company: Mapped[int] = mapped_column(ForeignKey("companies.id"))
    id_role: Mapped[int] = mapped_column(ForeignKey("roles.id"))

    user: Mapped[User] = relationship(back_populates="employments")
    company: Mapped[Company] = relationship(back_populates="employments")
    role: Mapped[Role] = relationship(back_populates="employments")


class VehicleType(enum.StrEnum):
    passenger = "passenger"
    cargo = "cargo"
    special = "special"


class Vehicle(Base):
    __tablename__ = "vehicles"

    # Базовые идентификаторы
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    company_id: Mapped[int] = mapped_column(
        ForeignKey("companies.id", ondelete="CASCADE")
    )

    # Юридическая информация
    license_plate: Mapped[str] = mapped_column(String(9))

    # Технические характеристики
    make: Mapped[str] = mapped_column(String(50))
    model: Mapped[str] = mapped_column(String(50))
    year: Mapped[int]
    vehicle_type: Mapped[VehicleType]
    carrying_capacity: Mapped[int | None]
    passenger_capacity: Mapped[int | None]
    fuel_consumption_rate: Mapped[float | None]

    # Эксплуатационные данные
    current_mileage: Mapped[int | None]
    initial_cost: Mapped[float | None]
    rent_price: Mapped[float | None]

    # Системные метаданные
    created_at: Mapped[date] = mapped_column(server_default=func.current_date())
    updated_at: Mapped[date] = mapped_column(
        server_default=func.current_date(), onupdate=func.current_date()
    )
    created_by: Mapped[int | None] = mapped_column(ForeignKey("users.id"))

    # ORM-отношения
    company: Mapped[Company] = relationship(back_populates="vehicles")
    creator: Mapped[User] = relationship()
    expenses: Mapped[Set["Expense"]] = relationship(back_populates="vehicle")


class ExpenseCategory(Base):
    __tablename__ = "expense_categories"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), unique=True)  # Топливо, Ремонт и т.д.
    code: Mapped[str] = mapped_column(String(10), unique=True)  # FUEL, REPAIR

    # Отношение "один ко многим"
    expenses: Mapped[list["Expense"]] = relationship(back_populates="category")


class ExpenseStatus(enum.StrEnum):
    pending = "pending"
    rejected = "rejected"
    approved = "approved"


class Expense(Base):
    __tablename__ = "expenses"

    # Базовые идентификаторы
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    company_id: Mapped[int] = mapped_column(
        ForeignKey("companies.id", ondelete="CASCADE")
    )

    # Финансовые данные
    amount: Mapped[float]

    # Временные метки
    expense_date: Mapped[date] = mapped_column(default=func.current_date())
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), onupdate=func.now()
    )

    # Связи с другими сущностями
    category_id: Mapped[int | None] = mapped_column(ForeignKey("expense_categories.id"))
    vehicle_id: Mapped[int | None] = mapped_column(ForeignKey("vehicles.id"))
    driver_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"))
    created_by: Mapped[int] = mapped_column(ForeignKey("users.id"))
    approver_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"))

    # Описательные поля
    description: Mapped[str | None] = mapped_column(String(255))

    # Статус
    status: Mapped[ExpenseStatus] = mapped_column(
        String(20), default=ExpenseStatus.pending
    )  # pending/approved/rejected

    # ORM-отношения
    company: Mapped["Company"] = relationship(back_populates="expenses")
    category: Mapped["ExpenseCategory"] = relationship()
    vehicle: Mapped["Vehicle"] = relationship(back_populates="expenses")
    driver: Mapped["User"] = relationship(back_populates="expenses")
    creator: Mapped["User"] = relationship(foreign_keys=[created_by])
    approver: Mapped["User"] = relationship(foreign_keys=[approver_id])
