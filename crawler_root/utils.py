import json
from .settings import ANALYTICS_NAME
from .model import Model


def serialize_model(obj):
    if isinstance(obj, Model):
        data = [str(obj.server_id), obj.name, str(obj.number), str(obj.added)]
        return data
    else:
        raise TypeError("Type not serializable")


def log_analytics(analytics_dict):
    with open(f'crawler_root/{ANALYTICS_NAME}', 'w') as f:
        f.write(json.dumps(analytics_dict, indent=4, default=serialize_model))
