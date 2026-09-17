"""
Scenario: you're building NotificationSender for a product that alerts users through Email today. 
Product wants SMS and push notifications next quarter, and a Slack webhook integration is already on the roadmap after that. 
Each channel needs different configuration (an SMTP server for email, a phone-number-based API for SMS, a device token for push) 
and formats its message text differently.

Task: apply Strategy to this. 
Name the interface and the method it requires. 
Name at least two concrete strategy classes and what each one's constructor would need to hold. 
Describe what the context class (NotificationSender or similar) is responsible for, and what it is explicitly not responsible for. 
"""

from abc import ABC, abstractmethod

# Interface for Notification mediums- contract that every notification medium must satisfy
class NotificationSenderStrategy(ABC):

    @abstractmethod
    def send_notification(self, message: str):
        pass

# Concrete Class 1 - Only responsible for Email Notifications
class EmailNotification(NotificationSenderStrategy):
    def __init__(self, email_id):
        self.email_id = email_id

    def send_notification(self, message: str):
        return f"Email sent to {self.email_id}\n{message}"

# Concrete Class 2 - Only responsible for SMS Notifications
class SMSNotification(NotificationSenderStrategy):
    def __init__(self, phone_number):
        self.phone_number = phone_number

    def send_notification(self, message: str):
        return f"SMS sent to {self.phone_number}\n{message}"

# Class that holds Notification Strategy and delegates it.
# It holds the reference to strategy and calls it, instead of implementing the behaviour.
class NotificationClient:

    def __init__(self, strategy: NotificationSenderStrategy):
        self._strategy = strategy

    def set_strategy(self, strategy: NotificationSenderStrategy):
        self._strategy = strategy

    def send(self, message: str):
        return self._strategy.send_notification(message)

# Usage
client = NotificationClient(SMSNotification(phone_number=899712302))
resp = client.send("Your bank balance is € 97,000")
print(resp+"\n")

client.set_strategy(EmailNotification(email_id="khushal@gmail.com"))
resp = client.send("Your bank balance is € 97,000")
print(resp)