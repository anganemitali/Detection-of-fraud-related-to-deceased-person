from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True,autoincrement = True)

    name = db.Column(db.String,nullable=False,unique=False)
    gender = db.Column(db.String,nullable=False,unique=False)
    email = db.Column(db.String,nullable=False,unique=False)
    contact = db.Column(db.String,nullable=False,unique=False)
    uid = db.Column(db.String, unique=True, nullable=False)
    accounts = db.relationship('BankAccount')



class BankAccount(db.Model):
    __tablename__ = 'bank_account'
    id = db.Column(db.Integer, primary_key=True,autoincrement = True)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    account_no = db.Column(db.String, nullable=False)
    branch_id = db.Column(db.Integer, db.ForeignKey('bank_branch.id'))
    branch = db.relationship("BankBranch")


class BankBranch(db.Model):
    __tablename__ = 'bank_branch'
    id = db.Column(db.Integer, primary_key=True,autoincrement = True)
    
    ifsc = db.Column(db.String, nullable=False)
    url = db.Column(db.String,nullable=False)
    


class BankAck(db.Model):
    __tablename__ = "bank_acks"
    id = db.Column(db.Integer, primary_key=True,autoincrement = True)
    received_on = db.Column(db.DateTime, server_default=db.func.now())
    

    uid = db.Column(db.String, nullable=False)
    name = db.Column(db.String,nullable=False)
    branch_id = db.Column(db.Integer, db.ForeignKey('bank_branch.id'))
    branch = db.relationship("BankBranch")
    branch_ack_received = db.Column(db.Boolean,default=False)
    
    def to_dict(self):
        return {"uid":self.uid,
                "name":self.name,
                "received_on" : self.received_on,
                "ifsc" : self.branch.ifsc,
                "branch_ack_received" : self.branch_ack_received,
                
                
                }
    
    
