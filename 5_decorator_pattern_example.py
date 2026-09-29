from abc import ABC, abstractmethod

# component - main class and the decorators would implement
class Notifier(ABC):
    
    @abstractmethod
    def send(self, message: str) -> bool:
        ...

# concrete component - real, undecorated base function
class EmailNotifier(Notifier):
    def __init__(self, address: str):
        self._address = address
    
    def send(self, message: str) -> bool:
        print(f"To: {self._address}\nMessage:{message}")
        return True

# Base decorator
class NotifierDecorator(Notifier):
    def __init__(self, wrapped: Notifier):
        self._wrapped = wrapped
    
    def send(self, message: str) -> bool:
        return self._wrapped.send(message)

# decorators
class RetryDecorator(NotifierDecorator):
    def __init__(self, wrapped: Notifier, attempts: int = 3):
        super().__init__(wrapped)
        self._attempts = attempts
    
    def send(self, message:str) -> bool:
        for attempt in range(1, self._attempts+ 1):
            print(f"[retry] attempt {attempt}")
            if self._wrapped.send(message):
                return True
        
        return False

class LoggingDecorator(NotifierDecorator):
    def send(self, message: str) -> bool:
        print(f"[log] sending: {message}")
        result = self._wrapped.send(message)
        print(f"[log] result: {result}")
        return result

class RateLimitDecorator(NotifierDecorator):
    def __init__(self, wrapped: Notifier, max_per_run: int = 2):
        super().__init__(wrapped)
        self._max_per_run = max_per_run
        self._sent = 0
    
    def send(self, message: str) -> bool:
        if self._sent > self._max_per_run:
            print(f"[rate-limit] blocked")
            return False
        
        self._sent += 1 
        return self._wrapped.send(message)

notifier = LoggingDecorator(RetryDecorator(EmailNotifier('kk@gm.com')))
notifier.send("Your order has been released")
