from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.sql.expression import null, text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from config import settings
from send_mail import send_email


app = Flask(__name__)

ENV = 'dev'

if ENV == "dev":
    app.debug = True
    app.config["SQLALCHEMY_DATABASE_URI"] = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}/{settings.database_name}'
else:
    app.debug = False
    app.config["SQLALCHEMY_DATABASE_URI"] = ""


app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


# Models
class Feedback(db.Model):
    __tablename__ = "feedback"

    id = Column(Integer, primary_key=True)
    customer = Column(String(200), nullable=False, unique=True)
    dealer = Column(String(200), nullable=False)
    rating = Column(Integer, nullable=False)
    comments = Column(Text(), nullable=False)
    created_at = Column(
        TIMESTAMP(timezone=True), nullable=False, server_default=text("now()")
    )

    def __init__(self, customer, dealer, rating, comments):
        self.customer = customer
        self.dealer = dealer
        self.rating = rating
        self.comments = comments

# Routes
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/submit", methods=["POST"])
def submit():
    if request.method == "POST":
        customer = request.form["customer"].lower()
        dealer = request.form["dealer"]
        rating = request.form["rating"]
        comments = request.form["comments"]
        # print(customer, dealer, rating, comments)
        if customer == "" or dealer == "":
            return render_template("index.html", message="Please enter required fields")

        if db.session.query(Feedback).filter(Feedback.customer == customer).count() == 0:
            data = Feedback(customer, dealer, rating, comments)
            db.session.add(data)
            db.session.commit()
            send_email(customer, dealer, rating, comments)
            return render_template("success.html")

        return render_template("index.html", message="Thank you! Feedback previously submitted")

if __name__ == "__main__":
    app.run()
