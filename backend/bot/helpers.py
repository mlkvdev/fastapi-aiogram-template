import phonenumbers
from phonenumbers import NumberParseException

from backend.config.settings import settings


def get_bot_webhook_url():
    return f"{settings.BASE_URL}/v1/bot/webhook"


def validate_phone_number(phone_number):
    try:
        z = phonenumbers.parse(phone_number, region='UZ')
        if phonenumbers.is_valid_number(z):
            return str(z.country_code) + str(z.national_number)
        return None
    except NumberParseException:
        return None
