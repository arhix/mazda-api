
from apiflask import abort, APIBlueprint
from flask import redirect, url_for

import pymazda
import os

from .mock_client import MockClient
from .schemas import MazdaAuth, DoorsStatus
from .auth import JWTAuth

bp = APIBlueprint('foo', __name__)

auth = JWTAuth(os.getenv('SECRET_KEY'))

useMock = os.getenv("MOCK_CLIENT", 'False').lower() in ('true', '1', 't')
mazdaClient = MockClient if useMock else pymazda.Client

@bp.post("/auth")
@bp.doc(summary='Get auth tocken', tag="auth")
@bp.input(MazdaAuth)
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


@bp.get("/vehicles")
@bp.doc(summary='List of vehicles', security='bearerAuth', tag="main")
@auth.login_required
async def getVehicles() -> None:
    client = mazdaClient(**auth.current_user)
    vehicles = await client.get_vehicles()
    await client.close()
    return vehicles


@bp.get("/vehicle/status/<int:vid>")
@bp.doc(summary='Vehicle status', security='bearerAuth', tag="main")
@auth.login_required
async def getStatus(vid: int) -> None:
    client = mazdaClient(**auth.current_user)
    status = await client.get_vehicle_status(vid)
    await client.close()
    return status


@bp.get("/doors/status/<int:vid>")
@bp.doc(summary='Check doors', security='bearerAuth', tag="doors")
@bp.output(DoorsStatus)
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


@bp.get("/doors/lock/<int:vid>")
@bp.doc(summary='Lock doors', security='bearerAuth', tag="doors")
@auth.login_required
async def lockDoors(vid: int) -> None:
    client = mazdaClient(**auth.current_user)
    await client.lock_doors(vid)
    await client.close()


@bp.get("/doors/unlock/<int:vid>")
@bp.doc(summary='Unlock doors', security='bearerAuth', tag="doors")
@auth.login_required
async def unlockDoors(vid: int) -> None:
    client = mazdaClient(**auth.current_user)
    await client.unlock_doors(vid)
    await client.close()


@bp.get("/lights/on/<int:vid>")
@bp.doc(summary='Hazard lights on', security='bearerAuth', tag="lights")
@auth.login_required
async def turn_on_hazard_lights(vid: int) -> None:
    client = mazdaClient(**auth.current_user)
    await client.turn_on_hazard_lights(vid)
    await client.close()


@bp.get("/lights/off/<int:vid>")
@bp.doc(summary='Hazard lights off', security='bearerAuth', tag="lights")
@auth.login_required
async def turn_off_hazard_lights(vid: int) -> None:
    client = mazdaClient(**auth.current_user)
    await client.turn_off_hazard_lights(vid)
    await client.close()


@bp.get("/engine/start/<int:vid>")
@bp.doc(summary='Start engine', security='bearerAuth', tag="engine")
@auth.login_required
async def startEngine(vid: int) -> None:
    client = mazdaClient(**auth.current_user)
    await client.start_engine(vid)
    await client.close()


@bp.get("/engine/stop/<int:vid>")
@bp.doc(summary='Stop engine', security='bearerAuth', tag="engine")
@auth.login_required
async def stopEngine(vid: int) -> None:
    client = mazdaClient(**auth.current_user)
    await client.stop_engine(vid)
    await client.close()
