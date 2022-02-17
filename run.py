from app.server import app

if __name__ == "__main__":
    # note: for development, i.e when you `pipenv run python3 ./app/server.py`
    app.run(host="localhost", port=3000, debug=True, access_log=True)
