import datetime


def check_for_pass_expire(expire_date):
    return True if (expire_date - datetime.date.today()).days <= 0 else False
