from .settings import ANALYTICS_NAME
from flask import Flask
import matplotlib.pyplot as plt
import json

app = Flask(__name__)


@app.route('/')
def show_analytics():
    with open(ANALYTICS_NAME, 'r') as f:
        data = json.load(f)
        plt.plot(1, 2, 4, 5, 6, 7, 8, 9)
        plt.plot(6, 2, 3, 3, 3, 3, 3 ,3)
        plt.savefig("analytics.png")
        return data
