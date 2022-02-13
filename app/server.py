from sanic import Sanic, text, request

app = Sanic(name="api")


@app.route("/")
async def home(request):
    return text("Hello World Sunday")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, debug=True)

# 22:25 + 3 + 2 ~= 22:29 should deployed or 4 mins
# 22:57 + 3 + 2 ~= 23:02