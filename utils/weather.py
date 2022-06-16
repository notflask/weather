import sys
import requests

from datetime import date, datetime
from dataclasses import dataclass
from enum import Enum
from typing import TypeAlias, Literal

from utils.exceptions import CannotParseResponse, CityNotSpecified
import utils.config

Celsius: TypeAlias = float

class WeatherType(str, Enum):
  THUNDERSTORM = "Гроза"
  DRIZZLE = "Мряка"
  RAIN = "Дощ"
  SNOW = "Сніг"
  CLEAR = "Ясно"
  FOG = "Туман"
  CLOUDS = "Хмарно"


@dataclass(slots = True, frozen = True)
class Weather:
  temperature: Celsius
  weather_type: WeatherType
  sunrise: datetime
  sunset: datetime
  city: str

def get_weather() -> Weather:
  # return f'''
  # {_get_city_from_args()}, температура 14°C, Облачно.
  # Восход: 20:54
  # Закат: 20:56
  # '''
  response = _get_api_response()
  weather = _parse_api_response(response)
  return weather

def _get_token() -> str:
  return utils.config.token

def _get_city_from_args() -> str:
  try:
    if "city" in sys.argv[1:][0]:
      return sys.argv[1:][1]
    else:
      raise CityNotSpecified
  except:
    raise CityNotSpecified

def _get_api_url(latitude: str, longitude: str) -> str:
  return utils.config.url.format(
    latitude = latitude,
    longitude = longitude
  )

def _get_coordinates(city: str) -> tuple:
  req = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={_get_token()}').json()
  
  lon = str(req["coord"]["lon"])
  lat = str(req["coord"]["lat"])

  return (lon, lat)

def _get_api_response() -> dict:
  coordinates = _get_coordinates(_get_city_from_args())
  req = requests.get(f'{_get_api_url(coordinates[1], coordinates[0])}')

  return req.json()

def _parse_api_response(response: dict) -> Weather:
  try:
    return Weather(
      temperature=_parse_temperature(response),
      weather_type=_parse_weather_type(response),
      sunrise=_parse_sun_time(response, "sunrise"),
      sunset=_parse_sun_time(response, "sunset"),
      city=_parse_city(response)
    )
  except:
    raise CannotParseResponse

def _parse_temperature(response: dict) -> Celsius:
  return round(response["main"]["temp"])

def _parse_weather_type(response: dict) -> WeatherType:
  try:
    weather_type_id = str(response["weather"][0]["id"])
  except (IndexError, KeyError):
    raise CannotParseResponse
  
  weather_types = {
    "1": WeatherType.THUNDERSTORM,
    "3": WeatherType.DRIZZLE,
    "5": WeatherType.RAIN,
    "6": WeatherType.SNOW,
    "7": WeatherType.FOG,
    "800": WeatherType.CLEAR,
    "80": WeatherType.CLOUDS
  }

  for _id, _weather_type in weather_types.items():
    if weather_type_id.startswith(_id):
      return _weather_type
  
  raise CannotParseResponse

def _parse_sun_time(response: dict, time: Literal["sunrise"] | Literal["sunset"]) -> datetime:
  return datetime.fromtimestamp(response["sys"][time])

def _parse_city(response: dict) -> str:
  try:
    return response["name"]
  except KeyError:
    raise CannotParseResponse
