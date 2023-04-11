from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return "This is the root of the app! Nothing to see here"