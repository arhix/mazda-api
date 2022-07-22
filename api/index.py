from apiflask import APIFlask, abort
import pymazda
import os

from .lib.mock_client import MockClient
from .lib.schemas import MazdaAuth, DoorsStatus
from .lib.auth import JWTAuth


app = APIFlask(__name__, title="MyMazda Api", version="0.2.0", docs_ui='elements')
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


auth = JWTAuth(app.secret_key)

useMock = app.debug and os.getenv("MOCK_CLIENT", 'False').lower() in ('true', '1', 't')
mazdaClient = MockClient if useMock else pymazda.Client

@app.route('/')
def index():
    return 'Index Page'

@app.post("/auth")
@app.doc(summary='Get auth tocken')
@app.input(MazdaAuth)
async def getAuth(data: MazdaAuth) -> None:
    client = mazdaClient(**data)
    try:
        await client.validate_credentials()
    except(Exception) as err:
        abort(401, message='Authentication error',
              extra_data={
                  'message': err
              })
    finally:
        client.close()

    return auth.encode(data)


@app.get("/vehicles")
@app.doc(summary='List of vehicles', security='bearerAuth')
@auth.login_required
async def getVehicles() -> None:
    client = mazdaClient(**auth.current_user)
    vehicles = await client.get_vehicles()
    await client.close()
    return vehicles


@app.get("/vehicle/status/<int:vid>")
@app.doc(summary='Vehicle status', security='bearerAuth')
@auth.login_required
async def getStatus(vid: int) -> None:
    client = mazdaClient(**auth.current_user)
    status = await client.get_vehicle_status(vid)
    await client.close()
    return status


@app.get("/doors/status/<int:vid>")
@app.doc(summary='Check doors', security='bearerAuth', tag="doors")
@app.output(DoorsStatus)
@auth.login_required
async def checkDoors(vid: int) -> None:
    client = mazdaClient(**auth.current_user)
    status = await client.get_vehicle_status(vid)
    await client.close()

    resp = DoorsStatus()
    if any(status['doors'].values()):
        resp.doorsClosed = False
        resp.doorsLocked = False
    elif any(status['doorLocks'].values()):
        resp.doorsLocked = False
    if any(status['windows'].values()):
        resp.windowsClosed = False
    return resp


@app.get("/doors/lock/<int:vid>")
@app.doc(summary='Lock doors', security='bearerAuth', tag="doors")
@auth.login_required
async def lockDoors(vid: int) -> None:
    client = mazdaClient(**auth.current_user)
    await client.lock_doors(vid)
    await client.close()


@app.get("/doors/unlock/<int:vid>")
@app.doc(summary='Unlock doors', security='bearerAuth', tag="doors")
@auth.login_required
async def unlockDoors(vid: int) -> None:
    client = mazdaClient(**auth.current_user)
    await client.unlock_doors(vid)
    await client.close()


@app.get("/lights/on/<int:vid>")
@app.doc(summary='Hazard lights on', security='bearerAuth', tag="lights")
@auth.login_required
async def turn_on_hazard_lights(vid: int) -> None:
    client = mazdaClient(**auth.current_user)
    await client.turn_on_hazard_lights(vid)
    await client.close()


@app.get("/lights/off/<int:vid>")
@app.doc(summary='Hazard lights off', security='bearerAuth', tag="lights")
@auth.login_required
async def turn_off_hazard_lights(vid: int) -> None:
    client = mazdaClient(**auth.current_user)
    await client.turn_off_hazard_lights(vid)
    await client.close()


@app.get("/engine/start/<int:vid>")
@app.doc(summary='Start engine', security='bearerAuth', tag="engine")
@auth.login_required
async def startEngine(vid: int) -> None:
    client = mazdaClient(**auth.current_user)
    await client.start_engine(vid)
    await client.close()


@app.get("/engine/stop/<int:vid>")
@app.doc(summary='Stop engine', security='bearerAuth', tag="engine")
@auth.login_required
async def stopEngine(vid: int) -> None:
    client = mazdaClient(**auth.current_user)
    await client.stop_engine(vid)
    await client.close()
