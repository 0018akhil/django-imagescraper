from django.shortcuts import render
from bs4 import BeautifulSoup
import requests
import os
import re
from django.core.files.base import ContentFile
from urllib.parse import urljoin

def mainView(req):

    if req.method == 'POST':
        url = req.POST.get('siteurl')
        download_image(url)

    return render(req, "index.html")

def sanitize_image_name(image_name):
    # Remove invalid characters from the image name using regex
    return re.sub(r'[/\\:*?"<>|]', '', image_name)

def download_image(url):
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        image_tags = soup.find_all('img')

        for img_tag in image_tags:
            img_url = img_tag.get('src')
            
            try:
                # Some image URLs may be relative, so resolve the full URL
                img_url = urljoin(url, img_url)

                # Download the image
                img_response = requests.get(img_url)
                if img_response.status_code == 200:
                    img_name = os.path.basename(img_url)
                    
                    # Sanitize the image name to remove invalid characters
                    img_name = sanitize_image_name(img_name)

                    img_content = ContentFile(img_response.content)

                    # Replace 'images' with the path to your desired directory for storing images
                    img_path = os.path.join('images', img_name)

                    # Save the image locally
                    with open(img_path, 'wb') as f:
                        f.write(img_content.read())
                else:
                    print(f"Failed to download image from URL: {img_url}")
            except Exception as e:
                print(f"Error while processing image URL: {img_url}")
                print(f"Error message: {str(e)}")


        print("Images downloaded successfully.")
    else:
        print("Failed to fetch the URL.")