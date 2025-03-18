from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime

app = Flask(__name__)

trainings = []


@app.route("/")
def index():
    return render_template("index.html", trainings=trainings)


@app.route("/add", methods=["GET", "POST"])
def add_training():
    global trainings
    if request.method == "POST":
        name = request.form.get('name', '').strip()
        date = request.form.get('date', '').strip()

        if not name or not date:
                return render_template('add_training.html', error="Name and date are required!")

        date_obj = datetime.strptime(date, "%Y-%m-%dT%H:%M")

        trainings.append({"name": name, "date": date_obj})
        return redirect(url_for("index"))

    return render_template("add_training.html")


@app.route("/delete/<int:index>", methods=["POST"])
def delete_training(index):
    global trainings
    if 0 <= index < len(trainings):
        del trainings[index]
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
