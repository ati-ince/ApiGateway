from fastapi import FastAPI

app = FastAPI(title="Service 2")

@app.get("/")
async def root():
    return {"message": "Service 2 is running"}

@app.get("/data")
async def get_data():
    return {
        "service": "Service 2",
        "data": [
            {"id": 4, "name": "Item 4"},
            {"id": 5, "name": "Item 5"},
            {"id": 6, "name": "Item 6"}
        ]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002) 