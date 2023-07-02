from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    password = db.Column(db.String(100))
    email = db.Column(db.String(120), unique=True)
    first_name = db.Column(db.String(100))
    last_name = db.Column(db.String(100))
    date_of_birth = db.Column(db.Date)
    address = db.Column(db.String(200))
    phone_number = db.Column(db.String(10))
    has_account = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return self.username

class Account(db.Model):
    account_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'))
    user = db.relationship('User', backref='accounts')
    balance = db.Column(db.Float)
    account_type = db.Column(db.String(100))
    is_active = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return str(self.account_id)

class Transaction(db.Model):
    transaction_id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.Integer, db.ForeignKey('account.account_id'))
    account = db.relationship('Account', backref='transactions')
    transaction_type = db.Column(db.String(100))
    amount = db.Column(db.Float)
    transaction_date = db.Column(db.Date)
    receiver_account_number = db.Column(db.String(20), nullable=True)

    def __repr__(self):
        return f"Transaction {self.transaction_id}"
