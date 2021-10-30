import os
import disnake
from text_moderator import TextModerator

import logging
logging.basicConfig(level=logging.INFO)

client = disnake.Client()
text_mod = TextModerator()  # Initialize the NLI Model


@client.event
async def on_ready():
    print(f'Logged in as {client.user}')


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.channel.id == 755079000962891891:  # use the channel ID where you want the bot to operate

        # TODO: Image Moderation
        # if len(message.attachments):
        #     for attachment in message.attachments:
        #         if os.path.splitext(attachment.filename)[1] in ['.jpg', '.png', '.jpeg']:

        #             # TODO: Use CLIP to filter the image
        #             raise NotImplementedError(
        #                 "Image Moderator not implemented yet")
        #             result, full_output = None, None
        #             logging.info(f"NLI Outputs on Message Text: {full_output}")

        #             await message.delete()
        #             await message.channel.send(f"{message.author.mention} This attachment was deleted as it contains `{result[1]}`.")

        # Text Moderation
        if len(message.content) > 3:

            result, full_output = text_mod.predict(message.content)
            logging.info(f"NLI Outputs on Message Text: {full_output}")

            if result[0]:
                await message.delete()
                await message.channel.send(f"{message.author.mention} This message was deleted as it contains `{result[1]}`.")

TOKEN = os.getenv('DISCORD')
if TOKEN is None:
    raise Exception(
        "Please assign your bot's token to the DISCORD environment variable.")
client.run(TOKEN)
