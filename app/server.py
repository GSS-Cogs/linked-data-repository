from sanic import Sanic, text, request

app = Sanic(name="api")


@app.route("/")
async def home(request):
    return text("Hello World Foo")

@app.route("/about")
async def home(request):
    return text("About Test")

@app.route("/helloworld3")
async def home(request):
    return text("Hello World3")

@app.route("/info")
async def home(request):
    return text("Info Test Last") 

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, debug=True)

# 22:25 + 3 + 2 ~= 22:29 should deployed or 4 mins
# 22:57 + 3 + 2 ~= 23:02