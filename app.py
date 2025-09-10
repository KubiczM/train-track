"""
train-track - A simple Flask web application for managing and displaying upcoming training sessions.

This application allows users to:
- View a list of upcoming trainings
- Add new trainings
- Edit existing trainings
- Delete trainings

The data is stored in a local JSON file and displayed on the website.

Features:
- Flask web framework for routing and rendering templates
- Simple JSON-based data storage for training sessions
- Basic CRUD (Create, Read, Update, Delete) functionality for managing training records
"""

from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
import json
import os

app = Flask(__name__)

TRAININGS_FILE = "trainings.json"


def load_trainings():
    if os.path.exists(TRAININGS_FILE):
        with open(TRAININGS_FILE, "r", encoding="utf-8") as file:
            try:
                data = json.load(file)
                return [
                    {
                        "name": t["name"],
                        "date": datetime.strptime(t["date"], "%Y-%m-%dT%H:%M"),
                    }
                    for t in data
                ]
            except json.JSONDecodeError:
                return []
    return []


def save_trainings():
    with open(TRAININGS_FILE, "w", encoding="utf-8") as file:
        json.dump(
            [
                {"name": t["name"], "date": t["date"].strftime("%Y-%m-%dT%H:%M")}
                for t in trainings
            ],
            file,
            ensure_ascii=False,
            indent=4,
        )


trainings = load_trainings()


@app.route("/")
def index():
    return render_template("index.html", trainings=trainings)


@app.route("/add", methods=["GET", "POST"])
def add_training():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        date = request.form.get("date", "").strip()

        if not name or not date:
            return render_template(
                "add_training.html", error="Name and date are required!"
            )

        date_obj = datetime.strptime(date, "%Y-%m-%dT%H:%M")

        trainings.append({"name": name, "date": date_obj})
        save_trainings()
        return redirect(url_for("index"))

    return render_template("add_training.html")


@app.route("/delete/<int:index>", methods=["POST"])
def delete_training(index):
    global trainings
    if 0 <= index < len(trainings):
        del trainings[index]
        save_trainings()
    return redirect(url_for("index"))


@app.route("/edit/<int:index>|", methods=["GET", "POST"])
def edit_training(index):
    if 0 <= index < len(trainings):
        training = trainings[index]

        if request.method == "POST":
            name = request.form.get("name", "").strip()
            date = request.form.get("date", "").strip()

            if not name or not date:
                return render_template(
                    "edit_training.html",
                    training=training,
                    index=index,
                    error="Name and date are required!",
                )

            training["name"] = name
            training["date"] = datetime.strptime(date, "%Y-%m-%dT%H:%M")
            save_trainings()
            return redirect(url_for("index"))

        return render_template("edit_training.html", training=training, index=index)

    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)