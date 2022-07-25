from aiohttp import ClientResponseError
from apiflask import abort, APIBlueprint
from flask import request
from pymazda.exceptions import *

import pymazda
import os

from api.lib.mock_client import MockClient
from api.lib.schemas import MazdaAuth, DoorsStatus
from api.lib.auth import JWTAuth

bp = APIBlueprint('foo', __name__)

auth = JWTAuth(os.getenv('SECRET_KEY'))

def getMazdaClient(request):
    debug = request.args.get('debug', 'false').lower() in ('true', '1', 't')
    useMock = os.getenv("MOCK_CLIENT", 'False').lower() in ('true', '1', 't')
    if useMock or debug:
        return MockClient
    return pymazda.Client

@bp.errorhandler(MazdaException)
@bp.errorhandler(MazdaConfigException)
@bp.errorhandler(MazdaAPIEncryptionException)
@bp.errorhandler(MazdaAuthenticationException)
@bp.errorhandler(MazdaAccountLockedException)
@bp.errorhandler(MazdaTokenExpiredException)
@bp.errorhandler(MazdaLoginFailedException)
def handle_mazda_request(err):
    abort(400, message=err.status)

@bp.post("/auth")
@bp.doc(summary='Get auth tocken', tag="auth")
@bp.input(MazdaAuth)
async def getAuth(data: MazdaAuth) -> None:
    client = None
    try:
        mazdaClient = getMazdaClient(request)
        client = mazdaClient(**data)
        await client.validate_credentials()
    except(
        MazdaException,
        MazdaConfigException,
        MazdaAPIEncryptionException,
        MazdaAuthenticationException,
        MazdaAccountLockedException,
        MazdaTokenExpiredException,
        MazdaLoginFailedException
    ) as err:
        abort(401, message='Authentication error', extra_data={
            'message': err.status
        })
    except(ClientResponseError) as err:
        abort(401, message='Authentication error', extra_data={
            'message': err.message
        })
    finally:
        if client is not None:
            client.close()

    return auth.encode(data)


@bp.get("/vehicles")
@bp.doc(summary='List of vehicles', security='bearerAuth', tag="main")
@auth.login_required
async def getVehicles() -> None:
    mazdaClient = getMazdaClient(request)
    client = mazdaClient(**auth.current_user)
    vehicles = await client.get_vehicles()
    await client.close()
    return vehicles


@bp.get("/vehicle/status/<int:vid>")
@bp.doc(summary='Vehicle status', security='bearerAuth', tag="main")
@auth.login_required
async def getStatus(vid: int) -> None:
    mazdaClient = getMazdaClient(request)
    client = mazdaClient(**auth.current_user)
    status = await client.get_vehicle_status(vid)
    await client.close()
    return status


@bp.get("/doors/status/<int:vid>")
@bp.doc(summary='Check doors', security='bearerAuth', tag="doors")
@bp.output(DoorsStatus)
@auth.login_required
async def checkDoors(vid: int) -> None:
    mazdaClient = getMazdaClient(request)
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


@bp.get("/doors/lock/<int:vid>")
@bp.doc(summary='Lock doors', security='bearerAuth', tag="doors")
@bp.output({}, 204)
@auth.login_required
async def lockDoors(vid: int) -> None:
    mazdaClient = getMazdaClient(request)
    client = mazdaClient(**auth.current_user)
    await client.lock_doors(vid)
    await client.close()
    return '', 204


@bp.get("/doors/unlock/<int:vid>")
@bp.doc(summary='Unlock doors', security='bearerAuth', tag="doors")
@bp.output({}, 204)
@auth.login_required
async def unlockDoors(vid: int) -> None:
    mazdaClient = getMazdaClient(request)
    client = mazdaClient(**auth.current_user)
    await client.unlock_doors(vid)
    await client.close()
    return '', 204


@bp.get("/lights/on/<int:vid>")
@bp.doc(summary='Hazard lights on', security='bearerAuth', tag="lights")
@bp.output({}, 204)
@auth.login_required
async def turn_on_hazard_lights(vid: int) -> None:
    mazdaClient = getMazdaClient(request)
    client = mazdaClient(**auth.current_user)
    await client.turn_on_hazard_lights(vid)
    await client.close()
    return '', 204


@bp.get("/lights/off/<int:vid>")
@bp.doc(summary='Hazard lights off', security='bearerAuth', tag="lights")
@bp.output({}, 204)
@auth.login_required
async def turn_off_hazard_lights(vid: int) -> None:
    mazdaClient = getMazdaClient(request)
    client = mazdaClient(**auth.current_user)
    await client.turn_off_hazard_lights(vid)
    await client.close()
    return '', 204


@bp.get("/engine/start/<int:vid>")
@bp.doc(summary='Start engine', security='bearerAuth', tag="engine")
@bp.output({}, 204)
@auth.login_required
async def startEngine(vid: int) -> None:
    mazdaClient = getMazdaClient(request)
    client = mazdaClient(**auth.current_user)
    await client.start_engine(vid)
    await client.close()
    return '', 204


@bp.get("/engine/stop/<int:vid>")
@bp.doc(summary='Stop engine', security='bearerAuth', tag="engine")
@bp.output({}, 204)
@auth.login_required
async def stopEngine(vid: int) -> None:
    mazdaClient = getMazdaClient(request)
    client = mazdaClient(**auth.current_user)
    await client.stop_engine(vid)
    await client.close()
    return '', 204
