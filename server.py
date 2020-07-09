import sentry_sdk

from bottle import Bottle, run
from sentry_sdk.integrations.bottle import BottleIntegration

import os

sentry_sdk.init(
    # Вместо <key и <project> необходимо ввести соответствующие вашему аккаунту данные
    dsn="https://<key>@sentry.io/<project>",
    integrations=[BottleIntegration()]
)

app = Bottle()


@app.route('/')
def index():
    return "Маршруты:\n" \
           "1. /success - Возвращает HTTP ответа со статусом 200 OK\n" \
           "2. /fail - Возвращает 'ошибку сервера'"


@app.route('/success')
def success():
    return "OK!"


@app.route('/fail')
def fail():
    raise RuntimeError("There is an error!")
    return


if os.environ.get("APP_LOCATION") == "heroku":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000)),
        server="gunicorn",
        workers=3,
    )
else:
    app.run(host="localhost", port=8080, debug=True)