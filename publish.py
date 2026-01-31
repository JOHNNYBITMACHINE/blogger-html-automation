import os
import re
import pickle
from googleapiclient.discovery import build

BLOG_ID = os.environ.get("BLOG_ID")
if not BLOG_ID:
    raise ValueError("BLOG_ID environment variable is missing")

def get_service():
    with open("token.pickle", "rb") as f:
        creds = pickle.load(f)
    return build("blogger", "v3", credentials=creds)

def read_html(path):
    with open(path, "r", encoding="utf-8") as f:
        html = f.read()

    title = re.search(r"title:\s*(.*)", html).group(1).strip()
    labels = re.search(r"labels:\s*(.*)", html).group(1)
    labels = [l.strip() for l in labels.split(",")]

    return title, html, labels

def publish_posts():
    service = get_service()
    for file in os.listdir("posts"):
        if file.endswith(".html"):
            title, html, labels = read_html(f"posts/{file}")

            service.posts().insert(
                blogId=BLOG_ID,
                body={
                    "title": title,
                    "content": html,
                    "labels": labels
                },
                isDraft=False
            ).execute()

            print(f"Published: {title}")

if __name__ == "__main__":
    publish_posts()
