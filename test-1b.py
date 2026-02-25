from fastapi import FastAPI, UploadFile, File, HTTPException
from elasticsearch import Elasticsearch
import json
import os

app = FastAPI()

ES_HOST = os.getenv("ES_HOST")
ES_USERNAME = os.getenv("ES_USER")
ES_PASSWORD = os.getenv("ES_PASSWORD")

missing_vars = []

if not ES_HOST:
    missing_vars.append("ES_HOST")
if not ES_USERNAME:
    missing_vars.append("ES_USER")
if not ES_PASSWORD:
    missing_vars.append("ES_PASSWORD")

if missing_vars:
    raise RuntimeError(
        f"Missing required environment variables: {', '.join(missing_vars)}"
    )

es = Elasticsearch(
    ES_HOST,
    basic_auth=(ES_USERNAME, ES_PASSWORD),
    verify_certs=True
)


INDEX_NAME = "rbcapp1-health"


@app.post("/add")
async def add_service_status(file: UploadFile = File(...)):
    try:
        content = await file.read()
        payload = json.loads(content)

        if not es.indices.exists(index=INDEX_NAME):
            es.indices.create(index=INDEX_NAME)

        es.index(index=INDEX_NAME, document=payload)


        return {"message": "Document indexed successfully"}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/healthcheck")
def get_all_health():
    try:
        aggs = {
            "services": {
                "terms": {"field": "service_name.keyword"},
                "aggs": {
                    "latest_status": {
                        "top_hits": {
                            "size": 1,
                            "sort": [{"@timestamp": {"order": "desc"}}]
                        }
                    }
                }
            }
        }

        result = es.search(index=INDEX_NAME, aggs=aggs, size=0)

        response = {}

        for bucket in result["aggregations"]["services"]["buckets"]:
            service = bucket["key"]
            latest_doc = bucket["latest_status"]["hits"]["hits"][0]["_source"]
            response[service] = latest_doc["service_status"]

        return response

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/healthcheck/{service_name}")
def get_service_health(service_name: str):
    try:
        query = {
            "term": {
                "service_name.keyword": service_name
            }     
        }
        sort=[{"@timestamp": {"order": "desc"}}]

        result = es.search(index=INDEX_NAME, query=query, sort=sort, size=1)

        if result["hits"]["total"]["value"] == 0:
            raise HTTPException(status_code=404, detail="Service not found")

        latest_doc = result["hits"]["hits"][0]["_source"]

        return {
            "service_name": service_name,
            "service_status": latest_doc["service_status"]
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
