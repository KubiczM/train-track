from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime

app = Flask(__name__)

trainings = []

@app.route('/')
def index():
    return render_template('index.html', trainings=trainings)

@app.route('/add', methods=['GET', 'POST'])
def add_event():
    if request.method == 'POST':
        name = request.form.get('name')
        date = request.form.get('date')

        try:
            date_obj = datetime.strptime(date, '%Y-%m-%d')
        except ValueError:
            return "Invalid date format! Use YYYY-MM-DD", 400

        trainings.append({'name': name, 'date': date_obj})
        return redirect(url_for('index'))

    return render_template('add_event.html')

if __name__ == '__main__':
    app.run(debug=True)
