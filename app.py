#!/usr/bin/env python3
from flask import Flask, jsonify
import time, random

app = Flask(__name__)

@app.route("/")
def index():
    return "Hello OTel from Flask!"

from opentelemetry import trace

@app.route("/work")
def work():
    span = trace.get_current_span()
    span.set_attribute("user.id", random.randint(1000, 9999))
    time.sleep(random.uniform(0.05, 0.25))
    return jsonify(status="ok")

import requests

@app.route("/chain")
def chain():
    r = requests.get("http://localhost:5000/work")
    return jsonify(downstream=r.json())

@app.route("/error")
def boom():
    raise RuntimeError("boom")

@app.route("/slow")
def slow():
    time.sleep(random.uniform(1.0, 2.0))
    return jsonify(status="done")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
