from aiogram.utils.i18n import I18n

from backend.config.settings import settings

i18n = I18n(path=settings.LOCALE_DIR, default_locale="en", domain="messages")
