import logging

logger = logging.getLogger(__name__)

def get_timestamp(t=None):
    dt = t if t else datetime.utcnow()
    return dt.isoformat() + 'Z'

