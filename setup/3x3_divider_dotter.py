import discord
from discord.ext import commands
from PIL import Image, ImageDraw
from io import BytesIO

# Set up your Discord bot (replace 'YOUR_BOT_TOKEN' with your actual bot token)
client = discord.Client()
TOKEN = ''
original_pieces = []
dotted_pieces = []


@client.event
async def on_ready():
    print(f'Logged in as {client.user.name}')

    channel = client.get_channel(1078045767262023740)

    if channel:
        await upload_pieces(channel)
        print("Extracted parts of original piece links:", original_pieces)
        print("Extracted parts of dotted piece links:", dotted_pieces)
    else:
        print("Channel not found")


async def upload_pieces(channel):
    image_path = r"C:\Users\bokch\Downloads\Racetrack.png"

    # Cut the image into 9 pieces and add dots, get the array
    pieces_with_dots_array = cut_and_add_dot(image_path)

    # Upload both pieces (with and without dots) to Discord channel
    for i, row in enumerate(pieces_with_dots_array):
        for j, (original_piece, piece_with_dot) in enumerate(row):
            # Save the original piece to a BytesIO object
            original_bytes = BytesIO()
            original_piece.save(original_bytes, format='PNG')
            original_bytes.seek(0)

            # Upload original piece to Discord channel
            original_file = discord.File(original_bytes, filename=f"empty_track_segment_{i}_{j}.png")
            message = await channel.send(file=original_file)

            attachment_url = message.attachments[0].url
            attachment_part = \
                attachment_url.split("https://cdn.discordapp.com/attachments/1078045767262023740/")[-1].split(".png")[
                    0] + ".png"
            original_pieces.append(attachment_part)

            # Save the piece with dot to a BytesIO object
            dot_bytes = BytesIO()
            piece_with_dot.save(dot_bytes, format='PNG')
            dot_bytes.seek(0)

            # Upload piece with dot to Discord channel
            dot_file = discord.File(dot_bytes, filename=f"dotted_track_segment_{i}_{j}.png")
            message = await channel.send(file=dot_file)

            # Extract attachment part from URL and append to the list
            attachment_url = message.attachments[0].url
            attachment_part = \
                attachment_url.split("https://cdn.discordapp.com/attachments/1078045767262023740/")[-1].split(".png")[
                    0] + ".png"
            dotted_pieces.append(attachment_part)


def cut_and_add_dot(image_path):
    img = Image.open(image_path)
    width, height = img.size
    square_width = width // 3
    square_height = height // 3
    pieces_array = [[None, None, None], [None, None, None], [None, None, None]]

    for i in range(3):
        for j in range(3):
            left = j * square_width
            upper = i * square_height
            right = left + square_width
            lower = upper + square_height

            # Original piece
            original_piece = img.crop((left, upper, right, lower))

            # Copy the original piece
            piece_with_dot = original_piece.copy()

            # Add a big red dot in the middle of the copied piece
            draw = ImageDraw.Draw(piece_with_dot)
            dot_radius = min(square_width, square_height) // 6
            dot_center = (square_width // 2, square_height // 2)
            draw.ellipse((dot_center[0] - dot_radius, dot_center[1] - dot_radius,
                          dot_center[0] + dot_radius, dot_center[1] + dot_radius),
                         fill="red")

            # Store the original piece and the piece with the dot in the array
            pieces_array[i][j] = (original_piece, piece_with_dot)

    return pieces_array


client.run(TOKEN)

