
def predict_rub_salary(payment_from, payment_to):
    if payment_from and payment_to:
        salary = (payment_from + payment_to) / 2
    elif payment_from:
        salary = payment_from * 1.2
    elif payment_to:
        salary = payment_to * 0.8
    else:
        salary = None
    return salary

