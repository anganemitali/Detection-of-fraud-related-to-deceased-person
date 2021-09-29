from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()


class StopAccount(db.Model):
    __tablename__ = 'stop_account'
    id = db.Column(db.Integer, primary_key=True,autoincrement = True)
    created_on = db.Column(db.DateTime, server_default=db.func.now())
    
    uid = db.Column(db.String, unique=True, nullable=False)
    account_no = db.Column(db.String, nullable=False)
    
