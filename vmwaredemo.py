import os
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from slack_sdk import WebClient
import openai

# Set up OpenAI API credentials
openai.api_type = "azure"
openai.api_base = "https://demounit12.openai.azure.com/"
openai.api_version = "2023-03-15-preview"
openai.api_key = os.getenv("OPENAI_API_KEY")

# Set up Slack API credentials
SLACK_BOT_TOKEN = os.environ.get("SLACK_BOT_TOKEN")
SLACK_APP_TOKEN = os.environ.get("SLACK_APP_TOKEN")
client = WebClient(token=SLACK_BOT_TOKEN)
app = App(token=SLACK_APP_TOKEN)

@app.event("app_mention")
def handle_message_events(body, logger):
    prompt = str(body["event"]["text"]).split(">")[1]

    response = client.chat_postMessage(channel=body["event"]["channel"],
                                       thread_ts=body["event"]["event_ts"],
                                       text=f"I'm on it!")

    chat_model_response = openai.ChatCompletion.create(
        engine="demounit04gpt",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}],
        max_tokens=300,
        top_p=0.5,
        frequency_penalty=0,
        presence_penalty=0,
        stop=None)

    chat_response_text = chat_model_response['choices'][0]['message']['content']

    replypost = client.chat_postMessage(channel=body["event"]["channel"],
                                       thread_ts=body["event"]["event_ts"],
                                       text=f"Here you go: {chat_response_text}")

if __name__ == "__main__":
    handler = SocketModeHandler(app, SLACK_APP_TOKEN)
    handler.start()
