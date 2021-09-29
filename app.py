from flask import Flask, request, jsonify, Response, render_template
from models import *

import requests

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///bank_dadar.sqlite"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
app.app_context().push()


@app.route("/stop_account",methods=["POST"])
def stop_account():
    recd = request.form
    sa = StopAccount(
                uid = recd["uid"],
                account_no = recd["account_no"]
            )
    
    db.session.add(sa)
    db.session.commit()
    
    return Response(status=200)

@app.route("/",methods=["GET"])
def home():
    sas = StopAccount.query.all()
    return render_template("home.html",sas=sas)

app.run(port=8002)
