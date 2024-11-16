from PIL import Image
import os


def crop_images(input_folder, valid_extensions):
    # Iterate through all files in the input folder
    for filename in os.listdir(input_folder):
        if filename.endswith(tuple(valid_extensions)):
            # Load the image
            image_path = os.path.join(input_folder, filename)
            img = Image.open(image_path)

            # Get the bounding box of non-zero pixels
            bbox = img.getbbox()

            # Crop the image using the bounding box
            cropped_img = img.crop(bbox)

            # Save the cropped image to the input folder (overwriting the original)
            cropped_img.save(image_path)


if __name__ == "__main__":
    input_folder = r"C:\Users\bokch\Downloads\password_icons"
    valid_extensions = ('.png', '.jpg', '.jpeg')

    crop_images(input_folder, valid_extensions)
