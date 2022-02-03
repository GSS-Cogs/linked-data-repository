from sanic import Sanic, text, request

app = Sanic(name="api")


@app.route("/")
async def home(request):
    return text("Hello World Sebastian")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, debug=True)
