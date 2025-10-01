from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import numpy as np

# telemetry
import json
import os

with open(os.path.join(os.path.dirname(__file__), "telemetry.json")) as f:
    TELEMETRY = json.load(f)

@app.post("/latency_metrics")
def get_latency_metrics(body: RequestBody):
    result = {}
    for region in body.regions:
        region_data = [r for r in TELEMETRY if r["region"] == region]
        if not region_data:
            continue

        latencies = [r["latency_ms"] for r in region_data]
        uptimes = [r["uptime_pct"] for r in region_data]
        breaches = sum(1 for l in latencies if l > body.threshold_ms)

        result[region] = {
            "avg_latency": float(np.mean(latencies)),
            "p95_latency": float(np.percentile(latencies, 95)),
            "avg_uptime": float(np.mean(uptimes)),
            "breaches": breaches
        }

    return result



