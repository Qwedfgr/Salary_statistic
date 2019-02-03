
def predict_rub_salary(payment_from, payment_to):
    if not (payment_from is None or payment_to is None):
        salary = (payment_from + payment_to) / 2
    elif payment_from is not None:
        salary = payment_from * 1.2
    elif payment_to is not None:
        salary = payment_to * 0.8
    else:
        salary = None
    return salary

