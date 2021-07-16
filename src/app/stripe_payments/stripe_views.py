import stripe
from flask import request, g, render_template
from . import stripe_payments
import os
from ..shared.auth_views import Auth
import json
from ..models import UserModel, StripeDetail, StripeSchema


@stripe_payments.route("/charge", methods=["POST"])
@Auth.auth_required
def charge():
    try:
        content = request.get_json()

        json_data = UserModel.get_one_user(g.user.get('id')).to_json()
        dict_data = json.loads(json_data)
        user_id = dict_data[0]["_id"]
        email = dict_data[0]["email"]
        
        resp = stripe.Charge.create(
            amount = content["amount"],
            currency = "inr",
            source = "tok_visa",
            receipt_email = email,
            description = "This is the sample payment"
        )
        # print("Success: %r" %(resp))
        payment = StripeDetail(
            user_id=user_id,
            payment_id=resp["id"],
            amount=resp["amount"]
        )
        payment.save()
        return {"message": 'Succesfully charged'}, 201
    except Exception as e:
        print(e)
        return "Transaction Failed", 500

@stripe_payments.route("/checkout", methods=["GET"])
@Auth.auth_required
def checkout(check_user, token):
    # try:
    json_data = UserModel.objects(_id=check_user).to_json()
    print(1111111111111111111111111, token)
    dict_data = json.loads(json_data)
    user_id = dict_data[0]["_id"]
    email = dict_data[0]["email"]

    session = stripe.checkout.Session.create(
    payment_method_types=['card'],
    line_items=[{
        'price': 'price_1J3guWSBtSTOsnXrTuA8fe2N',
        'quantity': 1,
        "description": "This the sample payment"
    }],
    mode='payment',
    success_url='http://127.0.0.1:5000/success',
    cancel_url='http://127.0.0.1:5000/cancel',
    )
    print("Success: %r" %(session))
    payment = StripeDetail(
        user_id=user_id,
        payment_id=session["id"],
        amount=session["amount"]
    )
    payment.save()
    return render_template("stripe/checkout.html")
    # except Exception as e:
    #     print(111111111111111111, e)
    #     return "Checkout Failed", 500

@stripe_payments.route("/success")
def success():
    return render_template("stripe/success.html")

@stripe_payments.route("/cancel")
def cancel():
    return "Cancel URL", 500