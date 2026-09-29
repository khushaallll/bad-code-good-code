from abc import ABC, abstractmethod
from typing import Optional

# Observer
class TempObserver(ABC):

    @abstractmethod
    def update(self, temp: float) -> None:
        ...

class DisplayPanel(TempObserver):
    def update(self, temp: float):
        print(f"[display] Temperature - {temp} degree celcius")

class FanController(TempObserver):
    def __init__(self, min_temp: float = None):
        self._min_temp = min_temp
    
    def update(self, temp: float):
        if temp < self._min_temp:
            print(f"[fan off] current temperature {temp} is too low")
        else:
            print(f"[fan on] current temperature {temp} is high")

class SafetyNotifier(TempObserver):
    def __init__(self, ph_no: str | None):
        self._ph_no = ph_no

    def update(self, temp: float):
        if temp > 30.0:
            print(f"[notify] Temperature warning sent to {self._ph_no}. ")

# Subject - Holds observers and notifies them when status changes
class TemperatureTracker:

    def __init__(self, temp: Optional[float]):
        self._temp = temp
        self._observers: list[TempObserver] = []

    def attach(self, observer: TempObserver):
        self._observers.append(observer)

    def detach(self, observer: TempObserver):
        self._observers.remove(observer)

    def _facilitate(self):
        for observer in list(self._observers):
            observer.update(self._temp)

    def tracked_temperature(self, temp: float):
        self._temp = temp
        self._facilitate()

# usage
tracker = TemperatureTracker()

display_obj = DisplayPanel()
fan_obj = FanController(16.2)
notifier_obj = SafetyNotifier("899999999")

tracker.attach(display_obj)
tracker.attach(fan_obj)
tracker.attach(notifier_obj)

tracker.tracked_temperature(32.00)

tracker.detach(notifier_obj)
tracker.tracked_temperature(32.00)