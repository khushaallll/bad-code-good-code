from abc import ABC, abstractmethod
from dataclasses import dataclass

# Some other function that we can't change
def fetch(lat, long):
    return {"temp_f": 71.6, "rh": 0.42, "summary": "clear"}

@dataclass
class WeatherReading:
    temperature_celsius: float
    humidity_percent: float
    description: str

# Target Interface
class WeatherClient(ABC):

    @abstractmethod
    def get_weather(self, lat: float, long: float) -> WeatherReading:
        pass

# Adapter Class
class LegacyMetClientAdapter(WeatherClient):
    def __init__(self):
        pass

    def get_weather(self, lat, long) -> WeatherReading:
        weather = fetch(lat, long)
        celsius = (weather["temp_f"] - 32) * 5/ 9
        percent = weather['rh'] * 100
        return WeatherReading(celsius, percent, weather["summary"])

        
class WeatherService:

    def __init__(self, weather_client: WeatherClient):
        self.weather_client = weather_client

    def get_current(self, lat: float, long: float):
        return self.weather_client.get_weather(lat, long)

weather_client = LegacyMetClientAdapter()
resp = WeatherService(weather_client).get_current(34.5, 56.7)
print(resp)

"""
WeatherService(weather_client).get_current(34.5, 56.7) — this is the only line that starts anything. It calls WeatherService.get_current.

get_current doesn't do any weather logic itself. It just says: "whatever weather_client I was given, ask it for the weather." So it calls self.weather_client.get_weather(lat, long). weather_client here is your LegacyMetClientAdapter instance — but WeatherService doesn't know that. It only knows it's holding something with a get_weather method, because that's what WeatherClient promises.

Now we're inside LegacyMetClientAdapter.get_weather. This is where the real work happens. First line: weather = fetch(lat, long). This calls the function you were told you can't change — the one that returns {"temp_f": 71.6, "rh": 0.42, "summary": "clear"}. This dict is in someone else's format. Fahrenheit, a 0–1 fraction, and the word "summary."

The next three lines fix that. celsius = (weather["temp_f"] - 32) * 5/9 turns 71.6°F into 22.0°C. percent = weather['rh'] * 100 turns 0.42 into 42.0. Then weather["summary"] — just pulled out as-is, no math needed, just picked up under a different name.

Last line: return WeatherReading(celsius, percent, weather["summary"]). You build a brand new WeatherReading object out of the three converted values, and hand that back.

So what actually happened: WeatherService asked a question in its own language ("get me the weather") and got an answer back in its own language (a WeatherReading with Celsius and percent). It never once touched Fahrenheit, never touched rh, never called fetch directly. All of that stayed inside LegacyMetClientAdapter.

That's what "adapter" means here. LegacyMetClientAdapter sits in the middle. On one side it knows how to talk to fetch — the messy, foreign format. On the other side it knows how to talk to WeatherService — through WeatherClient's get_weather method, which promises to always hand back a WeatherReading. It's the only class in your whole program that knows both languages. Everyone else only has to know one.

What you achieved: if tomorrow fetch got replaced by some other function with a totally different dict shape — say {"celsius": 22.0, "humidity_pct": 42.0, "condition": "clear"} — you would only ever touch LegacyMetClientAdapter. WeatherService and WeatherClient wouldn't change at all, because they were never written against fetch's shape in the first place — only against WeatherReading.
"""