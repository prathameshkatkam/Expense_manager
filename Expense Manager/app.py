from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import os

project_dir=os.path.dirname(os.path.abspath(__file__))
database_uri='postgresql://postgres:123454321@127.0.0.1:5432/myexpense'

app = Flask(__name__)

# Configure the database URI
app.config['SQLALCHEMY_DATABASE_URI'] = database_uri

# Create the SQLAlchemy instance with the app
db = SQLAlchemy(app)

class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(50), nullable=False)
    expensename = db.Column(db.String(50), nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    category = db.Column(db.String(50), nullable=False)

@app.route("/")
def add():
    return render_template('add.html')

@app.route("/addexpense", methods=['POST'])
def addexpense():
    date = request.form["date"]
    expensename = request.form["expensename"]
    amount = request.form["amount"]
    category = request.form["category"]

    expense=Expense(date=date,expensename=expensename,amount=amount,category=category)
    db.session.add(expense)
    db.session.commit()
    return redirect("/expenses")

@app.route("/expenses")
def expenses():
    expenses=Expense.query.all()
    total=0
    total_food=0
    total_entertainment=0
    total_other=0
    total_travel=0
    for expense in expenses:
        total+=expense.amount
        if expense.category=='travel':
            total_travel+=expense.amount
        elif expense.category=='other':
            total_other+=expense.amount
        elif expense.category=='food':
            total_food+=expense.amount
        if expense.category=='entertainment':
            total_entertainment+=expense.amount
    print(total_travel)
    return render_template("expenses.html",expenses=expenses,total=total,total_food=total_food,total_entertainment=total_entertainment,total_other=total_other,total_travel=total_travel)
    
@app.route("/delete/<int:id>")
def delete(id):
    expense=Expense.query.filter_by(id=id).first()
    db.session.delete(expense)
    db.session.commit()
    return redirect("/expenses")

@app.route("/update/<int:id>")
def update(id):
    expense=Expense.query.filter_by(id=id).first()
    return render_template("updateexpense.html",expense=expense)
@app.route("/edit",methods=["POST"])
def edit():
    id=request.form['id']
    date=request.form['date']
    expensename=request.form['expensename']
    amount=request.form['amount']
    category=request.form['category']

    expense=Expense.query.filter_by(id=id).first()
    expense.date=date
    expense.expensename=expensename
    expense.amount=amount
    expense.category=category

    db.session.commit()
    return redirect("/expenses")

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)