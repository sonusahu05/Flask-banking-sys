import datetime
from models import *
from flask import jsonify

def views_add_user(
        username,
        password,
        email,
        first_name,
        last_name,
        date_of_birth,
        address,
        phone_number
):
    new_user = User(
        username=username,
        password=password,
        email=email,
        first_name=first_name,
        last_name=last_name,
        date_of_birth=date_of_birth,
        address=address,
        phone_number=phone_number
    )
    db.session.add(new_user)
    db.session.commit()
    return "User "+ first_name +" added"

def get_account_details(acc_id):
    account = Account.query.filter_by(account_id=acc_id).first()
    if account:
        return jsonify({
            'account_id': account.account_id,
            'user_id': account.user_id,
            'balance': account.balance,
            'account_type': account.account_type,
            'is_active': account.is_active
        })
    else:
        return "No account found"

def add_account(account_type,balance,user_id):
    new_account = Account(
        account_type=account_type,
        balance=balance,
        user_id=user_id
    )
    db.session.add(new_account)
    db.session.commit()

    username = User.query.filter_by(user_id=user_id).first().username
    return "Account created for user "+ username +" added"


def get_accounts(account_id):
    accounts = Account.query.filter_by(account_id=account_id).all()
    if accounts:
        return jsonify(
            [
                {
                    'account_id': account.account_id,
                    'user_id': account.user_id,
                    'balance': account.balance,
                    'account_type': account.account_type,
                    'is_active': account.is_active
                }
                for account in accounts
            ]
        )
    else:
        return "No accounts found"
    
def deposit_amount(account_id,amount):
    account = Account.query.filter_by(account_id=account_id).first()
    if account:
        account.balance += amount
        db.session.commit()
        username= User.query.filter_by(user_id=account.user_id).first().username
        transaction = Transaction (
            account_id = account_id,
            amount = amount,
            transaction_type = "deposit",
            receiver_account_number=None,
            transaction_date = datetime.datetime.now(),
        )
        db.session.add(transaction)
        db.session.commit()
        return "Amount deposited Total balance: "+ str(account.balance) + " for account id: "+ str(account_id) + " for user: "+ username
    else:
        return "No account found"
    

def withdraw_amount(account_id,amount):
    account = Account.query.filter_by(account_id=account_id).first()
    if account:
        if account.balance >= amount:
            account.balance -= amount
            db.session.commit()
            username= User.query.filter_by(user_id=account.user_id).first().username
            transaction = Transaction (
                account_id = account_id,
                amount = amount,
                transaction_type = "withdraw",
                receiver_account_number=None,
                transaction_date = datetime.datetime.now(),
            )
            db.session.add(transaction)
            db.session.commit()
            return "Amount withdrawn Total balance: "+ str(account.balance) + " for account id: "+ str(account_id) + " for user: "+ username
        else:
            return "Insufficient balance"
    else:
        return "No account found"
    
def transfer_amount(sender_account_id,receiver_account_id,amount):
    sender_account = Account.query.filter_by(account_id=sender_account_id).first()
    receiver_account = Account.query.filter_by(account_id=receiver_account_id).first()
    if sender_account and receiver_account:
        if sender_account.balance >= amount:
            sender_account.balance -= amount
            receiver_account.balance += amount
            db.session.commit()
            sender_username= User.query.filter_by(user_id=sender_account.user_id).first().username
            receiver_username= User.query.filter_by(user_id=receiver_account.user_id).first().username
            transaction = Transaction (
                account_id = sender_account_id,
                amount = amount,
                transaction_type = "transfer",
                receiver_account_number=receiver_account_id,
                transaction_date = datetime.datetime.now(),
            )
            db.session.add(transaction)
            db.session.commit()
            return "Amount transferred Total balance: "+ str(sender_account.balance) + " for account id: "+ str(sender_account_id) + " for user: "+ sender_username + " to account id: "+ str(receiver_account_id) + " for user: "+ receiver_username
        else:
            return "Insufficient balance"
    else:
        return "No account found"