from datetime import datetime, timezone, timedelta

from services.common import check_for_pass_expire
from services.db import check_for_pass, get_expire_date, set_has_pass, clear_expire_date, add_months_for_pass, \
    check_if_user_registered
from services.pay import get_ony_plus_filtered_ranged_statements


def check_for_access(user_id):
    is_registered = check_if_user_registered(user_id)
    if is_registered:
        has_access = check_for_subscription(user_id)
        if has_access:
            return True
        return False
    return False


def check_for_subscription(user_id):
    has_pass = check_for_pass(user_id)
    if not has_pass:
        return False, None
    expire_date = get_expire_date(user_id)
    has_expired = check_for_pass_expire(expire_date)
    if has_expired:
        set_has_pass(user_id, False)
        clear_expire_date(user_id)
        return False, None
    return True, expire_date


def add_months_to_subscription(user_id, months):
    has_pass = check_for_pass(user_id)
    if not has_pass:
        set_has_pass(user_id, True)
    add_months_for_pass(user_id, months)


def get_last_minute_statements():
    time_now = datetime.now(timezone.utc)
    time_minus_one_minute = time_now - timedelta(minutes=1)
    return get_ony_plus_filtered_ranged_statements(int(time_minus_one_minute.timestamp()), int(time_now.timestamp()))
