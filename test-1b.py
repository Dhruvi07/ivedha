from fastapi import FastAPI, UploadFile, File, HTTPException
from elasticsearch import Elasticsearch
import json

app = FastAPI()

ES_HOST = "https://aghent-builder-f18136.kb.us-east-2.aws.elastic-cloud.com/"
ES_USERNAME = "elastic"
ES_PASSWORD = "GsfT********CgGH0J"

es = Elasticsearch(
    ES_HOST,
    basic_auth=(ES_USERNAME, ES_PASSWORD),
    verify_certs=False
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

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/healthcheck")
def get_all_health():
    try:
        query = {
            "size": 0,
            "aggs": {
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
        }

        result = es.search(index=INDEX_NAME, body=query)

        response = {}

        for bucket in result["aggregations"]["services"]["buckets"]:
            service = bucket["key"]
            latest_doc = bucket["latest_status"]["hits"]["hits"][0]["_source"]
            response[service] = latest_doc["service_status"]

        return response

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/healthcheck/{service_name}")
def get_service_health(service_name: str):
    try:
        query = {
            "size": 1,
            "query": {
                "match": {
                    "service_name": service_name
                }
            },
            "sort": [{"@timestamp": {"order": "desc"}}]
        }

        result = es.search(index=INDEX_NAME, body=query)

        if result["hits"]["total"]["value"] == 0:
            raise HTTPException(status_code=404, detail="Service not found")

        latest_doc = result["hits"]["hits"][0]["_source"]

        return {
            "service_name": service_name,
            "service_status": latest_doc["service_status"]
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
