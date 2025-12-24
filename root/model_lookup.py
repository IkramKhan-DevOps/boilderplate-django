from src.services.accounts.models import User
from src.services.management.models import Country, State

MODEL_CLASS_LOOKUP = {
    'accounts': {
        'user': User
    },
    'management': {
        'country': Country,
        'state': State,
    },
}
