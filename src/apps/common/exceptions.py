from dataclasses import dataclass


@dataclass(eq=False)
class ServiceException(Exception):
    @property
    def message(self):
        return 'Application exception occurred'


class ObjNotFoundException(ServiceException):
    @property
    def message(self):
        return 'Object not found'


class ObjAlreadyExistsException(ServiceException):
    @property
    def message(self):
        return 'Object already exists'
