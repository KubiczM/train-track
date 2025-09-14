from flask import Blueprint, render_template, request, redirect, url_for
from app.utils import load_trainings, save_trainings

main = Blueprint("main", __name__)

@main.route("/")
def index():
    trainings = load_trainings()
    return render_template("index.html", trainings=trainings)

@main.route("/add", methods=["GET", "POST"])
def add_training():
    if request.method == "POST":
        trainings = load_trainings()
        new_training = {
            "id": len(trainings) + 1,
            "title": request.form["title"],
            "date": request.form["date"],
            "time": request.form.get("time", ""),
            "notes": request.form.get("notes", "")
        }
        trainings.append(new_training)
        save_trainings(trainings)
        return redirect(url_for("main.index"))

    return render_template("add_training.html")


@main.route("/edit/<int:training_id>", methods=["GET", "POST"])
def edit_training(training_id):
    trainings = load_trainings()
    training = next((t for t in trainings if t["id"] == training_id), None)
    if not training:
        return "Training not found", 404

@main.route("/delete/<int:training_id>", methods=["POST"])
def delete_training(training_id):
    trainings = load_trainings()
    trainings = [t for t in trainings if t["id"] != training_id]
    save_trainings(trainings)
    return redirect(url_for("main.index"))

