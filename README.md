# ModBot

### A Chat Moderation Bot for Discord

ModBot is an AI powered general-purpose chat moderation discord bot which can be used to filter messages of any topic without any custom fine-tuning or training. It works out of the box for any topic to be filtered or restricted in a channel.

## How it works?

A distilbart model finetuned for natural language inference is repurposed for zero-shot text classification to classify messages into the filter categories. This makes the system work for almost all topics without the need of any fine-tuning on custom topics.

## Setup

1. Create your bot account and add it to your server. Make sure you give the bot the permissions to `manage messages` and enable the `message content` privileged intents.
2. Install the required python libraries with `pip install -r requirements.txt`.

## Usage

1. Set a `DISCORD` environment variable with your bot's secret client token.
2. Edit the [text_filters.txt](./text_filters.txt) file with the topics you want to restrict. Each new topic should be a new line.
3. Run the `modbot.py` script with `python modbot.py`. Voila! Your bot is not active and will automatically delete messages which belong to the topics mentioned in your filter.

## Use Cases

1. It can be used for filtering messages which contain hate speech, racism, or other such disrespectful slurs.
2. You can use this bot for keeping the chat of your users on-topic in a channel and remove off-topic messages.

## Disclaimer

- This is a purely experimental project and not ready for use in large communities. The AI used may contain social biases and can even wrongly delete messages.
- Ideally, if you want to deploy it to your discord server, you may want to implement a grievance system so users can report wrongfully deleted messages. You might also want to implement a feedback loop to improve the model overtime.
- All in all, use this model at your own risk.

## References

- https://huggingface.co/valhalla/distilbart-mnli-12-3
