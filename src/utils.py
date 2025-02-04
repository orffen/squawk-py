import math
import random
import urllib.request


def generate_squawk() -> str:
    """Generates a valid squawk code, excluding reserved codes."""
    code = "1200"
    while not is_valid_squawk(code):
        code = "".join(str(random.randint(0, 7)) for _ in range(4))
    return code


def is_valid_squawk(code: str) -> bool:
    """
    Checks if a squawk code is valid by comparing it to a list of reserved
    codes.
    """
    RESERVED_CODES = {
        21, 22, 25, 33, 500, 600, 700, 1200, 5061, 5062, 7001, 7004, 7615,
        *list(range(41, 58)), *list(range(100, 701)), *list(range(1200, 1278)),
        *list(range(4400, 4478)), *list(range(7501, 7578))
    }
    code_as_int = int(code)
    return not (
       not (0 < code_as_int <= 7777) or # range check
       code[-2:] == "00" or             # all codes ending in 00 are reserved
       code_as_int in RESERVED_CODES
    )


def retrieve_metar(icao: str) -> str:
    """
    Retrieve the current METAR/TAF information from a given set of ICAO codes.

    Can accept a list of codes separated by commas (e.g. "LOWI,EDDF,KJFK").
    """
    API_URL = "https://aviationweather.gov/api/data/metar?taf=true&ids="
    with urllib.request.urlopen(API_URL + icao) as response:
        if (response.status != 200):
            return "Error retrieving METAR, status code " + response.status
        metar = response.read().decode("utf-8")
        return metar if metar else f"NO METAR FOR {icao}"


def tod_calc_distance(current: int, target: int, angle: float=3) -> float:
    """
    Calculate the distance required for a given descent angle from a current
    to a target altitude.
    """
    _ft_in_nm = 6076
    # work with both '000s of feet or FLs
    current = current if current > 1000 else current * 1000
    target = target if target > 1000 else target * 1000
    if target >= current:
        return 0
    return (current - target) / (math.tan(math.radians(angle)) * _ft_in_nm)


def tod_calc_rate(ground_speed: int, angle: float=3) -> float:
    """
    Calculate the required descent rate in feet-per-minute for a given angle of
    descent.
    """
    if ground_speed < 0:
        return 0
    return ground_speed * math.tan(math.radians(angle)) * 60
