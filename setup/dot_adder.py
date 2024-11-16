from PIL import Image, ImageDraw


def add_red_dot(image, position):
    draw = ImageDraw.Draw(image)
    draw.ellipse(position, fill="red")
    del draw


def create_image_with_red_dot(original_image_path, output_folder):
    original_image = Image.open(original_image_path)

    # Define the size of each sub-image
    width, height = original_image.size
    sub_image_width = width // 3
    sub_image_height = height // 3

    for i in range(3):
        for j in range(3):
            # Create a copy of the original image
            new_image = original_image.copy()

            # Calculate the position of the red dot in the sub-image
            dot_x = (i + 0.5) * sub_image_width
            dot_y = (j + 0.5) * sub_image_height

            # Add the red dot to the sub-image
            add_red_dot(new_image, (dot_x - 50, dot_y - 50, dot_x + 50, dot_y + 50))

            # Save the modified image
            output_path = f"{output_folder}\dotted_track_{i}_{j}.png"
            new_image.save(output_path)


if __name__ == "__main__":
    original_image_path = r"C:\Users\bokch\Downloads\Racetrack.png"
    output_folder = r"C:\Users\bokch\Pictures\Tracks"

    create_image_with_red_dot(original_image_path, output_folder)
