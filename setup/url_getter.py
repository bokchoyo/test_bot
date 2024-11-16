import os
import discord
from discord.ext import commands

intents = discord.Intents.all()  # Enable all intents
client = commands.Bot(command_prefix="!", intents=intents)

folder_path = r"C:\Users\bokch\Pictures\Cars"


@client.event
async def on_ready():
    print(f'Logged in as {client.user.name} ({client.user.id})')

    channel = client.get_channel(1078045767262023740)
    await upload_files(channel)


async def upload_files(channel):
    if not os.path.exists(folder_path) or not os.path.isdir(folder_path):
        await channel.send("Invalid folder path.")
        return

    # Get a list of all files in the folder
    files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]

    # Upload each image to the channel
    for file in files:
        file_path = os.path.join(folder_path, file)
        with open(file_path, 'rb') as f:
            # Upload piece with dot to Discord channel
            filename = os.path.basename(file_path)
            file = discord.File(f, filename=filename)
            message = await channel.send(file=file)

            # Extract attachment part from URL and append to the list
            attachment_url = message.attachments[0].url
            attachment_part = \
                attachment_url.split("https://")[-1].split(".png")[0] + ".png"
            print(f"Uploaded: {attachment_part}")


# Replace 'TOKEN' with your actual bot token
client.run('')
