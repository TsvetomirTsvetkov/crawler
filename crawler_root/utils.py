import json
from .settings import ANALYTICS_NAME
from .model import Model


def log_analytics(analytics_dict):
    with open(ANALYTICS_NAME, 'w') as f:
        f.write(json.dumps(analytics_dict, indent=4, default=Model.serialize_model))
