import json
import matplotlib.pyplot as plt
from .settings import ANALYTICS_NAME_JSON, ANALYTICS_NAME_PNG
from .model import Model


def serialize_model(obj):
    if isinstance(obj, Model):
        data = [str(obj.server_id), obj.name, str(obj.number), str(obj.added)]
        return data
    else:
        raise TypeError("Type not serializable")


def log_analytics(analytics_dict):
    with open(f'crawler_root/saved_data/{ANALYTICS_NAME_JSON}', 'w') as f:
        f.write(json.dumps(analytics_dict, indent=4, default=serialize_model))
    analytics_diagram()


def analytics_diagram():
    with open(f'crawler_root/saved_data/{ANALYTICS_NAME_JSON}', 'r') as f:
        data = json.load(f)
    data_last_hour = len(data['LAST HOUR'])
    data_last_day = len(data['LAST DAY'])
    data_last_month = len(data['LAST MONTH'])

    fig = plt.figure(figsize=(6, 6))
    ax = fig.add_subplot(111)  # ax = fig.add_axes([0, 0, 1, 1])
    period = ['LAST MONTH', 'LAST DAY', 'LAST HOUR']
    period_data = [data_last_month, data_last_day, data_last_hour]
    ax.bar(period, period_data)
    ax.legend(['Number of new Servers'], loc='upper center', bbox_to_anchor=(0.5, 1.1))
    plt.savefig(f'crawler_root/saved_data/{ANALYTICS_NAME_PNG}')
