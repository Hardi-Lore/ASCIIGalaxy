import os
import json
import requests
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import random
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import base64
import numpy as np

def get_image_url(start_date=datetime(1995, 6, 16), end_date=datetime(2023, 11, 4)):
    """Generate a random date within the specified range and retrieve the corresponding APOD image URL.

    Args:
        start_date (datetime, optional): The start date for the date range. Defaults to datetime(1995, 6, 16).
        end_date (datetime, optional): The end date for the date range. Defaults to datetime(2023, 11, 4).

    Returns:
        str: The URL of the APOD image for the randomly selected date.
    """

    # Define the start and end dates
    # Note: The parameters start_date and end_date are already set as function arguments, no need to redefine them here.

    # Calculate the range of days between start and end dates
    date_range = (end_date - start_date).days

    # Generate a random number of days to add to the start date
    random_days = random.randint(0, date_range)

    # Calculate the random date
    random_date = start_date + timedelta(days=random_days)
    date_str = random_date.strftime("%y%m%d")

    # Construct the APOD URL components
    str_a = "https://apod.nasa.gov/apod/"
    str_a_ = "ap"
    str_b = ".html"

    # Combine the components to form the complete APOD URL for the randomly selected date
    sudo_image_url = str_a + str_a_ + date_str + str_b

    # Send a request to the APOD URL
    html = requests.get(sudo_image_url)

    # Parse the HTML content
    soup = BeautifulSoup(html.text, 'html.parser')

    # Find the image element in the HTML
    img = soup.find('img')

    # Extract the value of the 'src' attribute (image URL)
    src_value = img['src']

    # Combine the base URL and the extracted image URL to get the complete image URL
    image_url = str_a + src_value

    # Return the complete image URL
    return image_url

def get_check_image_url():
    """Retrieve a valid APOD image URL that ends with '.jpg'.

    Returns:
        str: A valid APOD image URL.
    """
    # Get an APOD image URL using the get_image_url function
    image_url = get_image_url()

    # Check if the image URL ends with '.jpg'
    if ".jpg" in image_url:
        # If it does, return the valid image URL
        return image_url
    else:
        # If not, recursively call the function to get another image URL
        return get_check_image_url()

def file_check(file_path="myfile.txt", file_path_base="myfile.txt", count=-1):
    """Check if a file exists at the specified path and generate a unique filename if needed.

    Args:
        file_path (str, optional): The path of the file to be checked. Defaults to "myfile.txt".
        file_path_base (str, optional): The base filename used for generating unique filenames. Defaults to "myfile.txt".
        count (int, optional): The current count of attempts to generate a unique filename. Defaults to -1.

    Returns:
        str: A unique filename that does not exist at the given path.
    """
    # Check if a file exists at the specified path
    if os.path.exists(file_path):
        # If it does, increment the count and generate a new filename
        count += 1
        parts = file_path_base.split(".")
        new_file_path = parts[0] + "_" + str(count) + "." + parts[1]

        # Recursive call to continue checking and generating until a unique filename is found
        return file_check(file_path=new_file_path, file_path_base=file_path_base, count=count)
    else:
        # If the file does not exist, return the original file path
        return file_path

def generate_file_name(file_path="myfile.txt"):
    """Generate a unique filename based on the provided file path.

    Args:
        file_path (str, optional): The initial file path. Defaults to "myfile.txt".

    Returns:
        str: A unique filename that does not exist at the specified path.
    """
    # Use the file_check function to generate a unique filename
    return file_check(file_path=file_path, file_path_base=file_path)

def generate_name():
    """Generate a name by combining a random present tense verb and a random noun.

    Returns:
        str: A randomly generated name.
    """
    # Load a dictionary of words from a JSON file
    with open("dict_of_words.json", "r") as json_file:
        dict_of_words = json.load(json_file)

    # Get a list of English present tense verbs
    present_tense_verbs = dict_of_words["present_tense_verbs"]
    # Get a list of English nouns
    nouns = dict_of_words["nouns"]

    # Combine a random present tense verb and a random noun to form the name
    name = random.choice(present_tense_verbs) + "_" + random.choice(nouns)

    # Return the generated name
    return name

def image_to_ascii(image_url, save_image=True, save_to="img/"):
    """Convert an image from the given URL into ASCII art.

    Args:
        image_url (str): The URL of the image to convert.
        save_image (bool, optional): Whether to save the ASCII art as an image file. Defaults to True.
        save_to (str, optional): The directory to save the image file. Defaults to "img/".

    Returns:
        tuple: If save_image is True, returns a tuple (ascii_art, file_name).
               If save_image is False, returns a tuple (encoded_img_data, file_name).
    """
    # Define the ASCII characters to use
    ASCII_CHARS = ['@', '%', '#', '*', '+', '=', '-', ':', '.', ' ']

    # Define the size of the ASCII block
    ASCII_BLOCK_SIZE = 10

    # Load the image from the URL
    response = requests.get(image_url)
    image = Image.open(BytesIO(response.content))

    # Convert the image to grayscale
    gray_image = image.convert('L')

    # Resize the image to the desired size
    width, height = gray_image.size
    new_width = int(width / ASCII_BLOCK_SIZE)
    new_height = int(height / ASCII_BLOCK_SIZE)
    resized_image = gray_image.resize((new_width, new_height))

    # Convert the image to a numpy array
    image_array = np.array(resized_image)

    # Convert the numpy array to ASCII block art
    ascii_art = ''
    for row in image_array:
        for pixel in row:
            ascii_art += ASCII_CHARS[int(pixel / (256 / len(ASCII_CHARS)))]

        ascii_art += '\n'

    # Convert the ASCII block art to a PIL image
    ascii_image = Image.new('RGB', (int(width * 0.6), int(height * 1.4)), color='white')  # white

    ascii_draw = ImageDraw.Draw(ascii_image)
    ascii_draw.text((0, 0), ascii_art, fill='black')  # black

    file_name = generate_name()

    if save_image:
        file_name_JPEG = save_to + file_name + ".jpg"
        output_filename = generate_file_name(file_path=file_name_JPEG)
        # Save the ASCII block art to a JPG file
        ascii_image.save(output_filename)
        ascii_image.close()

        return ascii_art, file_name

    if not save_image:
        data = BytesIO()
        ascii_image.save(data, "JPEG")
        encoded_img_data = base64.b64encode(data.getvalue())

        return encoded_img_data, file_name


    

# Example usage
if __name__ == "__main__":
    # Example usage:
    
    image_url = get_check_image_url()
    print(image_url)

    new_img_data, file_Name = image_to_ascii(image_url, save_image=True)
    print(new_img_data)








    




