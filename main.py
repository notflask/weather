from utils.weather import get_weather
from utils.formatter import format_weather

def main():
  weather = get_weather()
  formatted_weather = format_weather(weather)
  print(formatted_weather)

if __name__ == "__main__":
  main()