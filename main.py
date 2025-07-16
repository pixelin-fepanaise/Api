from fastapi import FastAPI
from fastapi.responses import JSONResponse
import json

app = FastAPI()

# Load your pre-generated JSON data (assume these files exist or are generated in the same folder)
with open("nodes.json", "r") as f:
    nodes_data = json.load(f)

with open("communities.json", "r") as f:
    communities_data = json.load(f)

with open("relationships.json", "r") as f:
    relationships_data = json.load(f)


@app.get("/")
def root():
    return {"message": "Welcome to the CDR Data API!"}


@app.get("/get-cdr-data-nodes-api")
def get_nodes():
    return JSONResponse(content={"statusCode": 200, "body": nodes_data})


@app.get("/get-cdr-data-communities-api")
def get_communities():
    return JSONResponse(content={"statusCode": 200, "body": communities_data})


@app.get("/get-cdr-data-relationships-api")
def get_relationships():
    return JSONResponse(content={"statusCode": 200, "body": relationships_data})
