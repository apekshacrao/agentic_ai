from flask import Flask, jsonify, redirect, render_template, request, url_for

from travel_agent import TravelAgent, load_places


app = Flask(__name__)
agent = TravelAgent(load_places())


@app.get("/")
def home():
    return render_template("index.html", destinations=agent.destinations())


@app.get("/results")
def results():
    details = {
        "people": request.args.get("people", 2),
        "days": request.args.get("days", 3),
        "budget": request.args.get("budget", 30000),
        "destination": request.args.get("destination", ""),
    }
    try:
        options = agent.destination_options(details)
    except ValueError as error:
        return render_template(
            "results.html", options=[], error=str(error), search=details
        )
    return render_template("results.html", options=options, error=None, search=details)


@app.route("/itinerary", methods=["GET", "POST"])
def itinerary():
    details = request.form.to_dict() if request.method == "POST" else request.args.to_dict()
    if not details:
        return redirect(url_for("home"))
    try:
        plan = agent.create_plan(details)
    except ValueError as error:
        return render_template("itinerary.html", plan=None, error=str(error))
    return render_template("itinerary.html", plan=plan, error=None)


@app.route("/booking", methods=["GET", "POST"])
def booking():
    submitted = request.method == "POST"
    return render_template("booking.html", submitted=submitted)


@app.get("/api/destinations")
def destinations():
    return jsonify({"destinations": agent.destinations()})


@app.get("/api/memory")
def memory():
    return jsonify({"trips": agent.memory})


@app.post("/api/plan")
def create_plan():
    data = request.get_json(silent=True) or {}
    try:
        plan = agent.create_plan(data)
    except ValueError as error:
        return jsonify({"error": str(error)}), 400
    return jsonify(plan)


if __name__ == "__main__":
    app.run(debug=True)
