import string

import random

from django.core.validators import RegexValidator


def secret_code():
    return string.digits


def secret_id(num):
    code = "TXNID" + "".join(random.choice(secret_code()) for _ in range(num))
    return code


def phone_validation():
    phone_validator = RegexValidator(
        regex=r"^[789]\d{7,9}$",
        message='Phone number must be in the format: "98XXXXXXXX" where X is a digit.',
    )
    return phone_validator
