import uvicorn

from api.ultimate import app

if __name__ == "__main__":
    # Run uvicorn server from inside docker
    uvicorn.run(app, host="localhost", port=8000)
