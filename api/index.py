from apiflask import APIFlask
import os

from .lib.routes import bp


app = APIFlask(__name__, title="MyMazda Api", version="0.2.0", docs_ui='elements', openapi_blueprint_url_prefix="/api", docs_path="/")
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
        'description': 'Feature Server',
        'url': 'https://{vercel_url}'.format(vercel_url=vercel_url)
    })

app.servers.append({
    'description': 'Public Server',
    'url': 'https://mazda-api.vercel.com'
})


app.register_blueprint(bp, url_prefix='/api')
