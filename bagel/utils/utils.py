import logging
import string
import random

from datetime import datetime

logger = logging.getLogger(__name__)

def get_timestamp(t=None):
    dt = t if t else datetime.utcnow()
    return dt.isoformat() + 'Z'

def random_string(length):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

