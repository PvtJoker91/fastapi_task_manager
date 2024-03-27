from abc import ABC, abstractmethod

from src.apps.users.entities.users import UserEntity


class BaseSenderService(ABC):
    @abstractmethod
    def send_message(self, user: UserEntity, message: str):
        ...


class EmailSenderService(BaseSenderService):
    def send_message(self, user: UserEntity, message: str):
        print(f"Message with account activate instructions '{message}' has sent to email '{user.email}'")



class SMSSenderService(BaseSenderService):
    def send_message(self, user: UserEntity, message: str):
        print(f"SMS with code '{message}' has sent to number '{user.phone}'")