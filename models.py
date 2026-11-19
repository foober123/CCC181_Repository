from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import CheckConstraint, DateTime, ForeignKey, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()


class Order(db.Model):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(primary_key=True)
    customer_name: Mapped[str] = mapped_column(String(120), nullable=False)
    address: Mapped[str | None] = mapped_column(Text, nullable=True)
    order_type: Mapped[str] = mapped_column(String(20), nullable=False)
    status: Mapped[str] = mapped_column(
        String(20),
        default="WAITING",
        server_default="WAITING",
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    items: Mapped[list["OrderItem"]] = relationship(
        back_populates="order",
        cascade="all, delete-orphan",
    )

    status_history: Mapped[list["OrderStatusHistory"]] = relationship(
        back_populates="order",
        cascade="all, delete-orphan",
        order_by="OrderStatusHistory.changed_at",
    )

    __table_args__ = (
        CheckConstraint(
            "order_type IN ('DELIVERY', 'WALK_IN')",
            name="ck_orders_order_type",
        ),
        CheckConstraint(
            "status IN ('WAITING', 'IN_TRANSIT', 'COMPLETE', 'CANCELLED')",
            name="ck_orders_status",
        ),
        

        CheckConstraint(
            """
            (
                order_type = 'WALK_IN'
                AND address IS NULL
            )
            OR
            (
                order_type = 'DELIVERY'
                AND address IS NOT NULL
                AND length(trim(address)) > 0
            )
            """,
            name="ck_orders_address_by_order_type",
        ),

    )


class OrderItem(db.Model):
    __tablename__ = "order_items"

    id: Mapped[int] = mapped_column(primary_key=True)
    order_id: Mapped[int] = mapped_column(
        ForeignKey("orders.id"),
        nullable=False,
    )
    product_name: Mapped[str] = mapped_column(String(120), nullable=False)
    quantity: Mapped[int] = mapped_column(nullable=False)

    order: Mapped["Order"] = relationship(back_populates="items")

    __table_args__ = (
        CheckConstraint(
            "quantity > 0",
            name="ck_order_items_quantity",
        ),
    )


class OrderStatusHistory(db.Model):
    __tablename__ = "order_status_history"

    id: Mapped[int] = mapped_column(primary_key=True)
    order_id: Mapped[int] = mapped_column(
        ForeignKey("orders.id"),
        nullable=False,
    )
    status: Mapped[str] = mapped_column(String(20), nullable=False)
    changed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    order: Mapped["Order"] = relationship(back_populates="status_history")

    __table_args__ = (
        CheckConstraint(
            "status IN ('WAITING', 'IN_TRANSIT', 'COMPLETE', 'CANCELLED')",
            name="ck_order_status_history_status",
        ),
    )
