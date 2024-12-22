from enum import Enum


class SubStatus(str, Enum):
    ACTIVE = 'ACTIVE'
    INACTIVE = 'INACTIVE'
    QUEUE = 'QUEUE'
    PENDING = 'PENDING'
