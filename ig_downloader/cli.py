import sys
import os
from ig_downloader.downloader import download_images

def main():
    args = sys.argv[1:]
    if not args:
        print("Usage: ig_downloader [urls.txt] or [URL1 URL2 ...]")
        sys.exit(1)

    urls = []
    if len(args) == 1 and os.path.isfile(args[0]):
        with open(args[0], 'r') as f:
            urls = [line.strip() for line in f if line.strip()]
    else:
        urls = args

    for url in urls:
        try:
            download_images(url)
        except Exception as e:
            print(f"Failed: {url}\n{e}")