import requests

class Weather:
  """ pass a valid api_key """
  def __init__(self, api_key):
      self.api_key = api_key

  def retrieveWeatherForecast(self, city):
      base_url = "http://api.openweathermap.org/data/2.5/weather"
      params = {
          "q": city,
          "appid": self.api_key,
          "units": "metric"
      }
  
      response = requests.get(base_url, params=params, verify=False)
      data = response.json()
  
      if data["cod"] == 200:
        weather_description = data["weather"][0]["description"]
        temperature = data["main"]["temp"]
        humidity = data["main"]["humidity"]
        wind_speed = data["wind"]["speed"]

        forecast = f"Weather forecast for {city}:\n" \
                f"Description: {weather_description}\n" \
                f"Temperature: {temperature}°C\n" \
                f"Humidity: {humidity}%\n" \
                f"Wind Speed: {wind_speed} meters/second"

        # print(f"{data}")
        return forecast
      else:
        # print(f"{data}")
        return "I could not retrieve weather forecast"

  """weatherPart [description|temperature|humidity|wind speed] """
  def retrieveWeatherForecastPart(self, city, weatherPart):
      base_url = "http://api.openweathermap.org/data/2.5/weather"
      params = {
          "q": city,
          "appid": self.api_key,
          "units": "metric"
      }
  
      response = requests.get(base_url, params=params, verify=False)
      data = response.json()
  
      if data["cod"] == 200:

        # print(f"{data}")
        infoLable = ""
        infoValue = ""
        forecast = ""
        if ("description" == weatherPart):
           infoLable = "description"
           infoValue = data["weather"][0]["description"]
        elif ("temperature" == weatherPart):
           infoLable = "temperature"
           infoValue = str(data["main"]["temp"]) + "°C"
        elif ("humidity" == weatherPart):
           infoLable = "humidity"
           infoValue = str(data["main"]["humidity"]) + "%"
        elif ("wind speed" == weatherPart):
           infoLable = "wind speed"
           infoValue = str(data["wind"]["speed"]) + " meters/second"
        forecast = f"Today's Weather {infoLable} in {city} is: {infoValue}\n"
        return forecast
      else:
        # print(f"{data}")
        return "I could not retrieve weather forecast"