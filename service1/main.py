from fastapi import FastAPI

app = FastAPI(title="Service 1")

@app.get("/")
async def root():
    return {"message": "Service 1 is running"}

@app.get("/data")
async def get_data():
    return {
        "service": "Service 1",
        "data": [
            {"id": 1, "name": "Item 1"},
            {"id": 2, "name": "Item 2"},
            {"id": 3, "name": "Item 3"}
        ]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001) 