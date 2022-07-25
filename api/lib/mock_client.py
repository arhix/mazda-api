from pprint import pprint


class MockClient:
    def __init__(self, email, password, region, websession=None, use_cached_vehicle_list=False):
        pprint([email, password, region, websession, use_cached_vehicle_list])

    async def validate_credentials(self):
        pass

    async def get_vehicles(self):
        return [
            {
                "vin": "JMXXXXXXXXXXXXXXX",
                "id": 12345,
                "nickname": "Nickname",
                "carlineCode": "C30",
                "carlineName": "CX-30 PREFERRED FWD",
                "modelYear": "2020",
                "modelCode": "C30  PF  2A",
                "modelName": "CX-30 WITH PREFERRED PACKAGE FWD",
                "automaticTransmission": True,
                "interiorColorCode": "D1P",
                "interiorColorName": "BLACK",
                "exteriorColorCode": "25D",
                "exteriorColorName": "SNOWFLAKE WHITE PEARL MC",
                "isElectric": False
            }
        ]

    async def get_vehicle_status(self, vehicle_id):
        return {
            "lastUpdatedTimestamp": "20210227145504",
            "latitude": 0.000000,
            "longitude": 0.000000,
            "positionTimestamp": "20210227145503",
            "fuelRemainingPercent": 18.0,
            "fuelDistanceRemainingKm": 79.15,
            "odometerKm": 3105.8,
            "doors": {
                "driverDoorOpen": False,
                "passengerDoorOpen": False,
                "rearLeftDoorOpen": False,
                "rearRightDoorOpen": False,
                "trunkOpen": False,
                "hoodOpen": False,
                "fuelLidOpen": False
            },
            "doorLocks": {
                "driverDoorUnlocked": False,
                "passengerDoorUnlocked": False,
                "rearLeftDoorUnlocked": False,
                "rearRightDoorUnlocked": False
            },
            "windows": {
                "driverWindowOpen": False,
                "passengerWindowOpen": False,
                "rearLeftWindowOpen": False,
                "rearRightWindowOpen": False
            },
            "hazardLightsOn": False,
            "tirePressure": {
                "frontLeftTirePressurePsi": 33.0,
                "frontRightTirePressurePsi": 35.0,
                "rearLeftTirePressurePsi": 33.0,
                "rearRightTirePressurePsi": 33.0
            }
        }

    async def close(self):
        pass

    async def start_engine(self, vid):
        pass

    async def stop_engine(self, vid):
        pass

    async def lock_doors(self, vid):
        pass

    async def unlock_doors(self, vid):
        pass
