from .subscription import SubscriptionModel


def get_base_model():
    from .base import BaseModel
    return BaseModel
