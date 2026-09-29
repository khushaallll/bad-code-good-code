from abc import ABC, abstractmethod

# Observer
class OrderObserver(ABC):

    @abstractmethod
    def update(self, order_id: str, status: str) -> None:
        # React to an order's status changing
        ...

class EmailNotifier(OrderObserver):
    def __init__(self, address: str):
        self._address = address

    def update(self, order_id: str, status: str) -> None:
        print(f"[email] to {self._address}: order {order_id} is now {status}")

class SMSNotifier(OrderObserver):
    def __init__(self, phone: str) -> None:
        self._phone = phone

    def update(self, order_id: str, status: str) -> None:
        print(f"[sms] to {self._phone}: order {order_id} is now {status}")

class WarehouseSystem(OrderObserver):
    def update(self, order_id: str, status: str) -> None:
        if status == "cancelled":
            print(f"[warehouse] restocking items for order {order_id}")
        elif status == "shipped":
            print(f"[warehouse] marking order {order_id} as dispatched")

# Subject - Holds observers and notifies them when status changes
class OrderTracker:

    def __init__(self, order_id: str) -> None:
        self._order_id = order_id
        self._status = 'placed'
        self._observers: list[OrderObserver] = []

    def attach(self, observer: OrderObserver) -> None:
        self._observers.append(observer)

    def detach(self, observer: OrderObserver) -> None:
        self._observers.remove(observer)

    def set_status(self, status: str):
        self._status = status
        self._notify()

    def _notify(self) -> None:
        for observer in self._observers:
            observer.update(self._order_id, self._status)

# usage
tracker = OrderTracker('A-1001')
tracker.attach(EmailNotifier("khush@gmail.com"))
tracker.attach(SMSNotifier("899999999"))
tracker.attach(WarehouseSystem())

tracker.set_status("shipped")