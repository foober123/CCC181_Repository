import os

from dotenv import load_dotenv
from flask import (
    Flask, abort, flash, redirect,
    render_template, request, url_for, jsonify
)
from flask_migrate import Migrate
from sqlalchemy import and_, or_
from sqlalchemy.exc import IntegrityError
from datetime import timedelta, timezone

from models import Order, OrderItem, OrderStatusHistory, db

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-only-change-me")

app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["DATABASE_URL"]
app.config["SQLALCHEMY_ECHO"] = os.environ.get("SQLALCHEMY_ECHO") == "1"

db.init_app(app)
migrate = Migrate(app, db)

PH_TIME = timezone(timedelta(hours=8))


@app.template_filter("local")
def local_time(value):
    """Display timestamps in Philippine time."""
    return (
        value.astimezone(PH_TIME).strftime("%b %d, %I:%M %p")
        if value else ""
    )


def get_people_ahead(order):
    """Count waiting orders of the same type placed before this order."""

    return Order.query.filter(
        Order.order_type == order.order_type,
        Order.status == "WAITING",
        or_(
            Order.created_at < order.created_at,
            and_(
                Order.created_at == order.created_at,
                Order.id < order.id
            )
        )
    ).count()



@app.route("/")
def index():
    filter_status = request.args.get("filter", "progress")

    query = Order.query

    if filter_status == "progress":
        query = query.filter(
            Order.status.in_(["WAITING", "IN_TRANSIT"])
        )

    elif filter_status == "1":
        query = query.filter(Order.status == "WAITING")

    elif filter_status == "2":
        query = query.filter(Order.status == "IN_TRANSIT")

    elif filter_status != "all":
        filter_status = "progress"
        query = query.filter(
            Order.status.in_(["WAITING", "IN_TRANSIT"])
        )

    orders = query.order_by(Order.created_at.asc(), Order.id.asc()).all()

    return render_template(
        "staff.html",
        name="Admin",
        tickets=orders,
        filter_status=filter_status
    )



@app.get("/queue/<int:ticket_id>")
def ticket(ticket_id):
    order = db.session.get(Order, ticket_id)

    if order is None:
        abort(404)

    ahead = get_people_ahead(order)

    return render_template(
        "ticket.html",
        ticket=order,
        ahead=ahead
    )



@app.get("/api/tickets/<int:ticket_id>/status")
def ticket_status(ticket_id):
    order = db.session.get(Order, ticket_id)

    if order is None:
        abort(404)

    ahead = get_people_ahead(order)

    return jsonify({
        "ticket_number": order.id,
        "name": order.customer_name,
        "status": order.status,
        "people_ahead": ahead
    })



@app.get("/staff")
def staff_dashboard():
    order_type = request.args.get("order_type")

    query = Order.query.filter(
        Order.status.in_(["WAITING", "IN_TRANSIT"])
    )

    if order_type in ["DELIVERY", "WALK_IN"]:
        query = query.filter(Order.order_type == order_type)

    orders = query.order_by(
        Order.created_at.asc(),
        Order.id.asc()
    ).all()

    return render_template(
        "staff.html",
        queue=orders,
        selected=order_type
    )



@app.post("/tickets/<int:ticket_id>/<action>")
def update_ticket(ticket_id, action):
    order = db.session.get(Order, ticket_id)

    if order is None:
        abort(404)

    new_status = {
        "in-transit": "IN_TRANSIT",
        "complete": "COMPLETE",
        "cancel": "CANCELLED"
    }.get(action)

    if new_status is None:
        abort(404)

    # Only delivery orders can be marked in transit
    if action == "in-transit" and order.order_type != "DELIVERY":
        abort(400)

    order.status = new_status

    # Save status history
    history = OrderStatusHistory(
        order_id=order.id,
        status=new_status
    )

    db.session.add(history)

    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        flash("Unable to update order status.", "danger")
        return redirect(url_for("index"))

    flash(
        f"Order #{ticket_id} marked as {new_status}.",
        "success"
    )

    return redirect(url_for("index"))



@app.get("/join")
def join_form():
    return render_template("join.html", form={})



@app.post("/join")
def join():
    form = request.form

    name = form.get("name", "").strip().upper()
    order_type = form.get("order_type", "").strip().upper()
    address = form.get("address", "").strip() or None

    errors = {}

    if not name or len(name) > 120:
        errors["name"] = "Enter your name (up to 120 characters)."

    if order_type not in ["DELIVERY", "WALK_IN"]:
        errors["order_type"] = "Choose a valid order type."

    if order_type == "DELIVERY" and not address:
        errors["address"] = "Enter your delivery address."

    if address and order_type == "WALK_IN":
        address = None

    # Collect order items
    items = form.getlist("item[]")
    quantities = form.getlist("quantity[]")

    order_items = []

    if len(items) != len(quantities):
        errors["orders"] = "Invalid order items."

    else:
        for item, quantity in zip(items, quantities):
            item = item.strip()

            # Ignore completely empty rows
            if not item and not quantity:
                continue

            if not item:
                errors["orders"] = "Enter a product name."
                break

            if len(item) > 120:
                errors["orders"] = "Product names must be 120 characters or less."
                break

            if not quantity.isdigit() or int(quantity) <= 0:
                errors["orders"] = "Enter a valid quantity."
                break

            order_items.append(
                OrderItem(
                    product_name=item,
                    quantity=int(quantity)
                )
            )

    if not order_items:
        errors["orders"] = "Add at least one order item."

    if errors:
        flash("Please fix the highlighted fields.", "danger")

        return render_template(
            "join.html",
            form=form,
            errors=errors
        ), 400

    new_order = Order(
        customer_name=name,
        order_type=order_type,
        address=address,
        status="WAITING",
        items=order_items,
        status_history=[
            OrderStatusHistory(status="WAITING")
        ]
    )

    db.session.add(new_order)

    try:
        db.session.commit()

    except IntegrityError:
        db.session.rollback()

        flash("Something went wrong saving your order. Please try again.", "danger")

        return render_template(
            "join.html",
            form=form,
            errors={}
        ), 409

    flash(
        f"You joined the queue. Your order is #{new_order.id}.",
        "success"
    )

    return redirect(url_for("ticket", ticket_id=new_order.id))


# --------------------------------------------------
# HELLO
# --------------------------------------------------

@app.route("/hello")
def hello():
    return "Hello, CCC181!"


# --------------------------------------------------
# DATABASE SEED
# --------------------------------------------------

@app.cli.command("seed")
def seed():
    """Add sample orders if they don't already exist."""

    samples = [
        {
            "customer_name": "$RESTAURANT",
            "order_type": "DELIVERY",
            "address": "123 Main Street",
            "items": [
                ("Cola 1L", 5)
            ]
        },
        {
            "customer_name": "$BAR",
            "order_type": "DELIVERY",
            "address": "456 Bar Street",
            "items": [
                ("Vodka Case", 2)
            ]
        }
    ]

    for sample in samples:

        exists = db.session.scalar(
            db.select(Order).filter_by(
                customer_name=sample["customer_name"]
            )
        )

        if exists is not None:
            continue

        order = Order(
            customer_name=sample["customer_name"],
            order_type=sample["order_type"],
            address=sample["address"],
            status="WAITING",
            items=[
                OrderItem(
                    product_name=item,
                    quantity=quantity
                )
                for item, quantity in sample["items"]
            ],
            status_history=[
                OrderStatusHistory(status="WAITING")
            ]
        )

        db.session.add(order)

    try:
        db.session.commit()
        print("Sample orders and items are ready.")

    except IntegrityError:
        db.session.rollback()
        print("Unable to seed sample orders.")

@app.post("/staff/tickets/<int:ticket_id>/delete")
def delete_ticket(ticket_id):
    order = db.session.get(Order, ticket_id)

    if order is None:
        abort(404)

    db.session.delete(order)

    try:
        db.session.commit()
        flash(f"Order #{ticket_id} was deleted.", "warning")

    except IntegrityError:
        db.session.rollback()
        flash("Unable to delete this order.", "danger")

    return redirect(url_for("index"))


# --------------------------------------------------
# RUN APPLICATION
# --------------------------------------------------

if __name__ == "__main__":
    app.run(debug=True)
