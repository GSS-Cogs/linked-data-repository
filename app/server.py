import os
from typing import Union

from sanic import Sanic, text, request

from ldrshared.clients import PubSubClient, BaseMessage

app = Sanic(name="api")

SUBSRIPTION_NAME = os.environ.get("SUBSCRIPTION_NAME", None)
assert SUBSRIPTION_NAME, 'You need to export the name of the subscription via the env var "SUBSCRIPTION_NAME"'

TOPIC_NAME = os.environ.get("TOPIC_NAME", None)
assert TOPIC_NAME, 'You need to export the name of the subscription via the env var "TOPIC_NAME"'

client = PubSubClient()
client.subscribe(SUBSRIPTION_NAME)

@app.route("/")
async def home(request):
    return text("Message queue example, use /get_message and /put-message?message=<str>")


# Note: this'll be slow sometimes, its because we poll/pull futures for 10 seconds
# that's fine, we're not using messenging like this in production.
@app.route("/get-message")
async def get(request):
    message: Union[BaseMessage, None] = client.get_next_message()
    if message:
        client.confirm_received(message)
        return text(f'got message: {message.get()}')
    else:
        return text('no message in queue')


@app.route("/put-message")
async def put(request):
    message_text = request.args.get('message', None)
    if not message_text:
        return text('No put message provided, please use a url param of message=<str of message>')
    else:
        client.put_one_message(TOPIC_NAME, message_text)
        return text(f'Message "{message_text}" has been added to topic: "{TOPIC_NAME}".')




if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3000, debug=True)
