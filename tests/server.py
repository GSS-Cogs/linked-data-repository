# file: server.py
import random
from sanic import Sanic
from sanic.response import json

app = Sanic(name=str("_" + str(random.randint(0, 10000))))

@app.route('test')
async def test(request):
    return json({'hello': 'world'})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)