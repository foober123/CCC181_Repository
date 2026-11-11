"""CCC181 Week 2: a "Hello, Flask" starter app.

Run it with:
    flask --app app run --debug
then open http://127.0.0.1:5000
"""
from flask import Flask, render_template

app = Flask(__name__)

# Sample data for the demo. A real app would load this from a database later.
SERVICES = [
    {"id": 1, "name": "Incoming"},
    {"id": 2, "name": "Outgoing"},

]

STATUS = [
    {"id": 1, "name": "Waiting"},
    {"id": 2, "name": "In Transit"},
    {"id": 3, "name": "No Show"},
    {"id": 4, "name": "Complete"},

]

TICKETS = [
        {"number": 1, "name": "UUA-222", "service_id": 1, "status_id": 1},
        {"number": 2, "name": "AHH-133", "service_id": 2, "status_id": 2}

]

@app.route("/")
def index():
    services = {s["id"]: s["name"] for s in SERVICES}
    status = {s["id"]: s["name"] for s in STATUS}

    return render_template(
        "index.html",
        name="Admin",
        tickets=TICKETS,
        services=services,
        status=status
    )

@app.route("/queue/<int:ticket_id>")
def ticket(ticket_id):
    # <int:ticket_id> only matches numbers, so /queue/abc returns 404.
    return render_template("ticket.html", ticket_id=ticket_id)


@app.route("/hello")
def hello():
    # The plain-string version from the Routes slide.
    return "Hello, CCC181!"


if __name__ == "__main__":
    # Lets you also start the app with: python app.py
    app.run(debug=True)
