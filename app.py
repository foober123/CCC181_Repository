import os

from dotenv import load_dotenv
from flask import (
    Flask, abort, flash, redirect,
    render_template, request, url_for, jsonify
)
from flask_migrate import Migrate
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError

from models import Order, OrderItem, OrderStatusHistory, db

load_dotenv()

app = Flask(__name__)
app.secret_key = "dev-only-change-me"  # Week 11 moves this into an environment variable
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ["DATABASE_URL"]
app.config["SQLALCHEMY_ECHO"] = os.environ.get("SQLALCHEMY_ECHO") == "1"

db.init_app(app)
migrate = Migrate(app, db)

# Sample data for the demo. A real app would load this from a database later.
SERVICES = [
    {"id": 1, "name": "Delivery"},
    {"id": 2, "name": "Walk-in"},

]

STATUS = [
    {"id": 1, "name": "Waiting"},
    {"id": 2, "name": "In Transit"},
    {"id": 3, "name": "Complete"},
    {"id": 4, "name": "Cancelled"},
]

TICKETS = [
        {"number": 1, 
         "name": "$RESTAURANT", 
         "service_id": 1, 
         "status_id": 1,
         "orders": [
            {"item": "Cola 1L", "quantity": 5}
             ]
         },

        {"number": 2, 
         "name": "$BAR", 
         "service_id": 1, 
         "status_id": 1,
         "orders": [
            {"item": "Vodka Case", "quantity": 2}
             ]
         },
]

@app.route("/")
def index():
    services = {s["id"]: s["name"] for s in SERVICES}
    status = {s["id"]: s["name"] for s in STATUS}

    # Get selected filter from URL
    filter_status = request.args.get("filter", "progress")

    # Filter tickets on the server
    if filter_status == "progress":
        filtered_tickets = [
            t for t in TICKETS
            if t["status_id"] in (1, 2)
        ]

    elif filter_status == "1":
        filtered_tickets = [
            t for t in TICKETS
            if t["status_id"] == 1
        ]

    elif filter_status == "2":
        filtered_tickets = [
            t for t in TICKETS
            if t["status_id"] == 2
        ]

    elif filter_status == "all":
        filtered_tickets = TICKETS

    else:
        filter_status = "progress"
        filtered_tickets = [
            t for t in TICKETS
            if t["status_id"] in (1, 2)
        ]

    return render_template(
        "staff.html",
        name="Admin",
        tickets=filtered_tickets,
        services=services,
        status=status,
        filter_status=filter_status
    )

@app.get("/queue/<int:ticket_id>")
def ticket(ticket_id):
    t = next(
        (t for t in TICKETS if t["number"] == ticket_id),
        None
    )

    if t is None:
        abort(404)

    ahead = sum(
        1 for x in TICKETS
        if x["service_id"] == t["service_id"]
        and x["status_id"] == 1
        and x["number"] < t["number"]
    )

    service = next(
        s for s in SERVICES
        if s["id"] == t["service_id"]
    )

    status = {s["id"]: s["name"] for s in STATUS}

    return render_template(
        "ticket.html",
        ticket=t,
        service=service,
        ahead=ahead,
        status=status
    )

@app.get("/api/tickets/<int:ticket_id>/status")
def ticket_status(ticket_id):
    t = next(
        (t for t in TICKETS if t["number"] == ticket_id),
        None
    )

    if t is None:
        abort(404)

    ahead = sum(
        1 for x in TICKETS
        if x["service_id"] == t["service_id"]
        and x["status_id"] == 1
        and x["number"] < t["number"]
    )

    status = next(
        (s["name"] for s in STATUS if s["id"] == t["status_id"]),
        "Unknown"
    )

    return jsonify({
        "ticket_number": t["number"],
        "name": t["name"],
        "status": status,
        "people_ahead": ahead
    })


@app.get("/staff")
def staff_dashboard():
    service_id = request.args.get("service_id", type=int)

    # Waiting or Called tickets
    queue = [
        t for t in TICKETS
        if t["status_id"] in (1, 2)
    ]

    if service_id:
        queue = [
            t for t in queue
            if t["service_id"] == service_id
        ]

    names = {s["id"]: s["name"] for s in SERVICES}
    status = {s["id"]: s["name"] for s in STATUS}

    return render_template(
        "staff.html",
        queue=queue,
        services=SERVICES,
        names=names,
        status=status,
        selected=service_id
    )

@app.post("/tickets/<int:ticket_id>/<action>")
def update_ticket(ticket_id, action):

    new_status = {
        "in-transit": 2,
        "complete": 3,
        "cancel": 4
    }.get(action)

    t = next(
        (t for t in TICKETS if t["number"] == ticket_id),
        None
    )

    if t is None or new_status is None:
        abort(404)

    # In Transit is only allowed for Delivery
    if action == "in-transit" and t["service_id"] != 1:
        abort(400)

    t["status_id"] = new_status

    flash(
        f"Ticket #{ticket_id} marked as {STATUS[new_status - 1]['name']}.",
        "success"
    )

    return redirect(url_for("index"))

@app.get("/join")
def join_form():
    return render_template("join.html", services=SERVICES, form={})

@app.post("/join")
def join():
    form = request.form
    name = form.get("name", "").strip().upper()
    service_id = form.get("service_id", type=int)

    errors = {}

    if not name:
        errors["name"] = "Enter your name."

    if service_id not in [s["id"] for s in SERVICES]:
        errors["service_id"] = "Choose a service."

    # Get ordered items
    orders = []

    items = form.getlist("item[]")
    quantities = form.getlist("quantity[]")

    for item, quantity in zip(items, quantities):
        item = item.strip()

        if item and quantity.isdigit() and int(quantity) > 0:
            orders.append({
                "item": item,
                "quantity": int(quantity)
            })

    if not orders:
        errors["orders"] = "Add at least one order."

    if errors:
        flash("Please fix the highlighted fields.", "danger")
        return render_template(
            "join.html",
            services=SERVICES,
            form=form,
            errors=errors
        ), 400

    number = TICKETS[-1]["number"] + 1 if TICKETS else 1

    TICKETS.append({
        "number": number,
        "name": name,
        "service_id": service_id,
        "status_id": 1,
        "orders": orders
    })

    flash(f"You joined the queue. Your ticket is #{number}.", "success")

    return redirect(url_for("ticket", ticket_id=number))

@app.route("/hello")
def hello():
    # The plain-string version from the Routes slide.
    return "Hello, CCC181!"


if __name__ == "__main__":
    # Lets you also start the app with: python app.py
    app.run(debug=True)
