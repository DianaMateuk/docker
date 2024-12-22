from database.models.subscription import SubscriptionModel
from database.repositories.base import BaseRepository


class SubscriptionRepository(BaseRepository[SubscriptionModel]):
    def __init__(self):
        super().__init__(SubscriptionModel)
