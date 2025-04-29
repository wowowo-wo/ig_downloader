import requests
from bs4 import BeautifulSoup
import os
import re
import json

def extract_shared_data(html):
    shared_data_pattern = r"window\._sharedData = (.*?);</script>"
    match = re.search(shared_data_pattern, html)
    if match:
        json_data = match.group(1)
        return json.loads(json_data)
    return None

def extract_media_urls(shared_data):
    try:
        media = shared_data["entry_data"]["PostPage"][0]["graphql"]["shortcode_media"]
    except (KeyError, IndexError):
        return []

    urls = []
    if media.get("edge_sidecar_to_children"):
        for edge in media["edge_sidecar_to_children"]["edges"]:
            node = edge["node"]
            if node.get("is_video"):
                urls.append(node["video_url"])
            else:
                urls.append(node["display_url"])
    else:
        if media.get("is_video"):
            urls.append(media["video_url"])
        else:
            urls.append(media["display_url"])

    return urls

def download_file(url, save_folder):
    filename = url.split('?')[0].split('/')[-1]
    filepath = os.path.join(save_folder, filename)
    if os.path.exists(filepath):
        print(f"Skip(already exists): {filename}")
        return

    try:
        response = requests.get(url)
        response.raise_for_status()
        with open(filepath, 'wb') as f:
            f.write(response.content)
        print(f"Succeed: {filename}")
    except Exception as e:
        print(f"Failed: {filename}, Error: {e}")

def download_images(url, save_folder="./downloads"):
    if not os.path.exists(save_folder):
        os.makedirs(save_folder)

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    shared_data = extract_shared_data(response.text)
    media_urls = extract_media_urls(shared_data) if shared_data else []

    if not media_urls:
        og_image = soup.find('meta', property='og:image')
        if og_image and og_image.get('content'):
            media_urls = [og_image['content']]

    if media_urls:
        for media_url in media_urls:
            download_file(media_url, save_folder)
    else:
        print(f"Couldn't find any media at: {url}")