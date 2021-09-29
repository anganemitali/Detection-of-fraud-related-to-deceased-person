from flask import Flask, request, jsonify, Response, redirect, render_template, url_for
from models import *

import requests

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///municipal.sqlite"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
app.app_context().push()

uidai_url = "http://localhost:5001/municipal_request"

@app.route("/",methods=["GET"])
def home():
    if "mode" in request.args:
        mode = request.args['mode']
    else:
        mode = None
    records = Record.query.all()
    return render_template("home.html",records=records,mode=mode)


@app.route("/new_record",methods=["POST"])
def new_record():
    try:

        recd = request.form

        record = Record(
                     uid = recd["uid"],
                     name = recd["name"]
                 )

        db.session.add(record)
        db.session.commit()

        data = {"uid":recd["uid"]}
        x = requests.post(uidai_url,data=data)
        if x.status_code == 200:
            record.uidai_ack_received = True
            db.session.commit()
            return redirect(url_for("home",mode="submitted"))

        return redirect(url_for("home",mode="uidai_error"))

    except Exception:
        return redirect(url_for("home",mode="error"))
    




app.run(port=5000)
