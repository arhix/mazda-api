from apiflask import APIFlask
import os
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration

from api.lib.routes import bp

sentry_sdk.init(
    dsn=os.getenv('SENTRY_DSN'),
    integrations=[
        FlaskIntegration(),
    ],
    traces_sample_rate=1.0,
    environment = os.getenv('FLASK_ENV') or os.getenv('VERCEL_ENV') or "production",
)


app = APIFlask(__name__, title="MyMazda Api", version="0.2.0", docs_ui='elements', docs_path="/")
app.config.update(
    SECRET_KEY=os.getenv('SECRET_KEY'),
    DOCS_FAVICON='https://www.mazdausa.com/favicon.ico',
    SECURITY_SCHEMES={
        'bearerAuth': {
            'type': 'http',
            'scheme': 'bearer',
            'bearerFormat': 'JWT',
        }
    },
    ELEMENTS_CONFIG={
        'router': 'hash'
    }
)

app.servers = []
if app.debug:
    app.servers.append({
        'description': 'Local Server',
        'url': 'http://127.0.0.1:5000'
    })

vercel_env = os.getenv('VERCEL_ENV', "local")
vercel_url = os.getenv('VERCEL_URL')
if vercel_env != "production" and vercel_url is not None:
    app.servers.append({
        'description': 'Feature Server on Vercel',
        'url': 'https://{vercel_url}'.format(vercel_url=vercel_url)
    })

app.servers.append({
    'description': 'Public Server on Vercel',
    'url': 'https://mazda-api.vercel.app'
})

heroku_name = os.getenv('HEROKU_APP_NAME')
if heroku_name is not None:
    app.servers.append({
        'description': 'Feature Server on Heroku(💤)',
        'url': 'https://{heroku_name}.herokuapp.com'.format(heroku_name=heroku_name)
    })

app.servers.append({
    'description': 'Public Server on Heroku(💤)',
    'url': 'https://mazda-api.herokuapp.com'
})


app.register_blueprint(bp)
