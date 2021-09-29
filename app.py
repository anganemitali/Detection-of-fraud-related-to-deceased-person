#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 14 16:57:41 2020


"""

from flask import Flask, request, jsonify, Response, render_template
from models import *

import requests

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///uidai.sqlite"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
app.app_context().push()


@app.route("/municipal_request",methods=["POST"])
def municipal_request():
    try:
        recd = request.form
        uid = recd["uid"]

        user = User.query.filter_by(uid=uid).first()
        accounts = user.accounts

        for account in accounts:
            print("Sending info to ifsc: " + account.branch.ifsc)

            url = account.branch.url
            data = {"uid":uid,"account_no":account.account_no}
            x = requests.post(url, data = data)
            bank_ack = BankAck(uid=uid,branch=account.branch,name=user.name)
            db.session.add(bank_ack)
            db.session.commit() 
            if x.status_code == 200:
                bank_ack.branch_ack_received = True
                db.session.commit()
            
        return Response(status=200)
    except Exception:
        return Response(status=500)

        
           


@app.route("/find_ack",methods=["POST"])
def find_ack():
    uid = request.form["uid"]
    acks = BankAck.query.filter_by(uid=uid).all()
# =============================================================================
#     acks = [obj.to_dict() for obj in acks_query]
# =============================================================================
    return render_template("home.html",bas=acks,uid=uid)

@app.route("/",methods=["GET"])
def home():
    bas = BankAck.query.all()
    return render_template("home.html",bas=bas)

app.run(port=5001)
