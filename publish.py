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

def parse_html(path):
    with open(path, "r", encoding="utf-8") as f:
        html = f.read()

    post_id = re.search(r"post_id:\s*(.*)", html).group(1).strip()
    title = re.search(r"title:\s*(.*)", html).group(1).strip()
    labels = re.search(r"labels:\s*(.*)", html).group(1)
    labels = [l.strip() for l in labels.split(",")]

    return post_id, title, html, labels

def save_post_id(path, post_id):
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()

    content = re.sub(
        r"post_id:\s*",
        f"post_id: {post_id}",
        content,
        count=1
    )

    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

def publish_all_posts():
    service = get_service()

    for file in os.listdir("posts"):
        if not file.endswith(".html"):
            continue

        path = f"posts/{file}"
        post_id, title, html, labels = parse_html(path)

        body = {
            "title": title,
            "content": html,
            "labels": labels
        }

        if post_id:
            service.posts().update(
                blogId=BLOG_ID,
                postId=post_id,
                body=body
            ).execute()
            print(f"✏️ Updated: {title}")

        else:
            post = service.posts().insert(
                blogId=BLOG_ID,
                body=body,
                isDraft=False
            ).execute()

            save_post_id(path, post["id"])
            print(f"🆕 Created: {title}")

if __name__ == "__main__":
    publish_all_posts()
