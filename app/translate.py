import json
import requests
from urllib.parse import quote_plus

from flask_babel import _

from flask import current_app


def translate(text, sourse_lang, dest_lang):
    if 'MS_TRANSLATOR_KEY' not in current_app.config or not current_app.config['MS_TRANSLATOR_KEY']:
        return _("Error: Translation service is not configured")

    r = requests.get('https://translate.yandex.net/api/v1.5/tr.json/translate'
                     '?key={}&text={}&lang={}'.format(current_app.config['MS_TRANSLATOR_KEY'],
                                                      quote_plus(text), sourse_lang + '-' + dest_lang))

    if r.status_code != 200:
        return _("Error: Translation service failed")

    return json.loads(r.content.decode('utf-8-sig'))["text"][0]
