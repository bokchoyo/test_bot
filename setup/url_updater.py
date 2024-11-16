import discord
import os
from glob import glob
from car_database import CarDatabase

car_db = CarDatabase()

# Your Discord bot token
TOKEN = ''

# Your Discord channel ID
CHANNEL_ID = 1078045767262023740

# Path to the folder containing pictures
PICTURE_FOLDER = 'C:/Users/bokch/Pictures/Cars'

client = discord.Client()

# List to store the extracted parts of attachment links
attachment_parts = []
attachment_part_lengths = []


@client.event
async def on_ready():
    print(f'We have logged in as {client.user.name}')

    # await car_db.create_car_database()
    # await car_db.add_car('Lamborghini Revuelto',
    #                      '',
    #                      'Arancio Borealis', 'Lamborghini', 'Revuelto',
    #                      2024, 85.69, 608400, 'A', 'Supercar', 40,
    #                      217.5, 2.4, 1001, 535, 3907,
    #                      350, 2.5, 1015, 725, 1772)
    # await car_db.add_car('Ferrari SF90 Stradale',
    #                      '',
    #                      'Rosso Corsa', 'Ferrari', 'SF90 Stradale',
    #                      2019, 83.90, 524900, 'A', 'Supercar', 40,
    #                      211, 2.4, 986, 590, 3461,
    #                      340, 2.5, 1000, 800, 1570)
    # await car_db.add_car('Ford Mustang EcoBoost Fastback',
    #                      '1195068102359134258/4.png?ex=65b2a4e6&is=65a02fe6&hm=43ea2c8575c57d13ce6dc2a8a4457fad4c4ae02ac962a8394ac05980dbf0f583&',
    #                      'Oxford White', 'Ford', 'Mustang EcoBoost Fastback',
    #                      2024, 31.68, 31000, 'D', 'Sports Car', 10,
    #                      145, 4.5, 315, 350, 3588,
    #                      233, 4.7, 319, 475, 1627)
    # await car_db.add_car('Chevrolet Camaro 1LS',
    #                      '1195094252485607565/9.png?ex=65b2bd41&is=65a04841&hm=5fa679e87997e3e723bc1e3d6532c81fab1d0d02453b17051fe307a74a6c98a8&',
    #                      'Summit White', 'Chevrolet', 'Camaro 1LS',
    #                      2019, 22.59, 26400, 'D', 'Sports Car', 10,
    #                      149, 5.4, 275, 295, 3351,
    #                      240, 5.6, 279, 400, 1520)
    # await car_db.add_car('Aston Martin DB12',
    #                      '1195111385605095444/10.png?ex=65b2cd36&is=65a05836&hm=dea2ed4a4c088630a89a3725ff25dbd4382f5c80559347b1d8b9ed2c3cd6eb65&',
    #                      'Iridescent Emerald', 'Aston Martin', 'DB12',
    #                      2024, 70.86, 248100, 'B', 'Supercar', 25,
    #                      202, 3.4, 671, 590, 3715,
    #                      325, 3.5, 680, 800, 1685)
    # await car_db.add_car('Audi R8 GT',
    #                      '1195261544452337704/11.png?ex=65b3590f&is=65a0e40f&hm=6bb5a051f686db94160379c46caac98d4ab68fcd4dc7c7c186e2bae853db505b&',
    #                      'Suzuka Gray', 'Audi', 'R8 GT',
    #                      2023, 72.61, 249900, 'B', 'Supercar', 25,
    #                      199, 3.2, 602, 413, 3516,
    #                      320, 3.3, 610, 560, 1595)
    # await car_db.add_car('Honda Civic Type R',
    #                      '',
    #                      '', 'Honda', 'Civic Type R',
    #                      2022, 35.19, 44900, 'C', 'Hatchback', 15,
    #                      170, 4.9, 602, 413, 3516,
    #                      274, 5.1, 610, 560, 1595)

    # Get the specified channel
    channel = client.get_channel(CHANNEL_ID)

    # Check if the channel is found
    if channel:
        # Upload all pictures in the folder
        await upload_pictures(channel)

        # Print the extracted parts of attachment links
        print("Extracted parts of attachment links:", attachment_parts)
        print("Attachment link lengths:", attachment_part_lengths)
    else:
        print(f'Channel with ID {CHANNEL_ID} not found.')

    await car_db.set_image_urls(attachment_parts)


async def upload_pictures(channel):
    picture_files = glob(os.path.join(PICTURE_FOLDER, '*.png')) + glob(os.path.join(PICTURE_FOLDER, '*.jpg'))
    # picture_files.sort(key=lambda x: int(os.path.basename(x).split('.')[0]))

    # Upload each picture to the channel
    for picture_file in picture_files:
        with open(picture_file, 'rb') as file:
            # Create a File object for the image with a specified filename
            picture_filename = os.path.basename(picture_file)
            picture = discord.File(file, filename=picture_filename)

            # Send the picture to the channel
            message = await channel.send(file=picture)

            # Extract the part of the attachment link until right after ".png"
            attachment_url = message.attachments[0].url
            attachment_part = \
                attachment_url.split("https://cdn.discordapp.com/attachments/1078045767262023740/")[-1].split(".png")[
                    0] + ".png"

            # Append to the list in order of upload
            attachment_parts.append(attachment_part)
            attachment_part_lengths.append(len(attachment_part))


# Run the bot
client.run(TOKEN)
