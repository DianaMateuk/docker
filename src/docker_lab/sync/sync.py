from itertools import zip_longest
from logging import info

from nexium_google.utils import ServiceAccount

from database.repositories import SubscriptionRepository
from nexium_google.spreadsheet import Spreadsheet, BaseRowModel, Field, FieldType
from utils.config import GOOGLE_SPREADSHEET_WORKSHEET_TITLE, ID, USERNAME, FULLNAME, PHONE, \
    SUB_TYPE, SUB_STATUS, GOOGLE_SPREADSHEET_ID


class SubscriptionRowModel(BaseRowModel):
    __sheet__ = GOOGLE_SPREADSHEET_WORKSHEET_TITLE
    id = Field(title=ID, type_=FieldType.INTEGER, nullable=False)
    username = Field(title=USERNAME, type_=FieldType.STRING, nullable=False)
    fullname = Field(title=FULLNAME, type_=FieldType.STRING, nullable=False)
    phone = Field(title=PHONE, type_=FieldType.INTEGER, nullable=False)
    sub_type = Field(title=SUB_TYPE, type_=FieldType.STRING, nullable=False)
    sub_status = Field(title=SUB_STATUS, type_=FieldType.STRING, nullable=False)


spreadsheet = Spreadsheet(
    service_account=ServiceAccount(filename='creds.json'),
    id_=GOOGLE_SPREADSHEET_ID,
    models=[SubscriptionRowModel],
)

async def sync():
    info('Start syncing')
    rows = await SubscriptionRowModel().get_all()
    subscription_repo = SubscriptionRepository()
    subscriptions = await subscription_repo.get_all()
    new_subscription = SubscriptionRowModel()
    for subscription, row in zip_longest(subscriptions, rows, fillvalue=new_subscription):
        data = {
            'id': subscription.id,
            'username': subscription.username,
            'fullname': subscription.fullname,
            'phone': int(subscription.phone),
            'sub_type': subscription.sub_type,
            'sub_status': subscription.sub_status,
        }
        if row != new_subscription:
            info('check for update')
            have_changes = False
            for k, i in data.items():
                if getattr(row, k) == data[k]:
                    continue
                have_changes = True
                setattr(row, k, data[k])
            if have_changes:
                info('updating')
                await row.update()
                info('updated')
        else:
            info('Adding new row')
            for k, i in data.items():
                setattr(new_subscription, k, data[k])

            await row.create()
            info('New row added')
    info('Sync finished')