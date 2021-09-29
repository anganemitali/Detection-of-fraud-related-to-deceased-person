#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 14 15:54:40 2020


"""

from flask import Flask
from models import *

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///uidai.sqlite"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
app.app_context().push()

db.drop_all()
db.create_all()

import pandas as pd

pd.set_option("display.max_columns",None)
df = pd.read_csv("customer data.csv",
                 dtype={"contact no.":str,"acc no":str})
df.columns = ["name","gender","email","contact","uid","ifsc","account_no"]
df.drop(0,inplace=True)

df["name"] = df["name"].fillna("unknown")
df["gender"] = df["gender"].fillna("u")
df["ifsc"] = df["ifsc"].fillna("unknown")

df["uid"] = df["uid"].str.replace(" ","").str.strip()

user = df[["name","gender","email","contact","uid"]]
user = user.dropna()

user["id"] = list(range(1,len(user)+1))
user = user[["id","uid","name","gender","email","contact"]]



branch = df[["ifsc"]].copy()
ifsc_url_mapping = {}

unique_branches = list(branch["ifsc"].unique())

for index,ifsc in enumerate(unique_branches,1):
    port = 8000 + index
    url = "http://localhost:" + str(port) + "/stop_account"
    ifsc_url_mapping[ifsc] = url

branch["url"] = branch["ifsc"].map(ifsc_url_mapping)
branch["id"] = list(range(1,len(branch)+1))
branch = branch[["id","ifsc","url"]]

bank_account = df[["uid","account_no","ifsc"]]
bank_account = bank_account.ffill()
bank_account["id"] = list(range(1,len(bank_account)+1))

def get_user_id(x):
    a = user[user["uid"]==x]
    return a.iloc[0,0]

def get_branch_id(x):
    a = branch[branch["ifsc"]==x]
    return a.iloc[0,0]

bank_account["user_id"] = bank_account["uid"].map(get_user_id)
bank_account["branch_id"] = bank_account["ifsc"].map(get_branch_id)
bank_account = bank_account[["id","user_id","account_no","branch_id"]]



user.to_sql(
        "user",
        db.engine,
        if_exists='append',
        index=False,
        dtype = {
                    "id" : db.Integer(),
                    "uid" : db.String(),
                    "email" : db.String(),
                    "contact" : db.String(),
                    "gender" : db.String(),
                    "name" : db.String()
                }
        )
branch.to_sql(
        "bank_branch",
        db.engine,
        if_exists='append',
        index=False,
        dtype = {
                     "id" : db.Integer(),
                     "ifsc" : db.String(),
                     "url" : db.String(),
                }
        )

bank_account.to_sql(
        "bank_account",
        db.engine,
        if_exists='append',
        index=False,
        dtype = {
                     "id" : db.Integer(),
                     "user_id" : db.Integer(),
                     "account_no" : db.String(),
                     "branch_id" : db.Integer()
                }
        )




db.session.commit()
