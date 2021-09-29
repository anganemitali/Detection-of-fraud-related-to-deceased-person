from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()


class Record(db.Model):
    __tablename__ = 'record'
    id = db.Column(db.Integer, primary_key=True,autoincrement = True)
    created_on = db.Column(db.DateTime, server_default=db.func.now())
    
    uid = db.Column(db.String, unique=True, nullable=False)
    name = db.Column(db.String, nullable=False)
    uidai_ack_received = db.Column(db.Boolean,default=False)
    