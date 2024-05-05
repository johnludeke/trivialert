import os
import praw
from time import sleep
from slack_bolt import App

# Initialize your app with your bot token and signing secret
app = App(
    token = os.environ.get("SLACK_BOT_TOKEN"),
    signing_secret = os.environ.get("SLACK_SIGNING_SECRET"),
)

channel_id = "YOUR_CHANNEL_ID_HERE"

# Initialize the Reddit API client
reddit = praw.Reddit(
    client_id = os.environ.get("REDDIT_CLIENT_ID"),
    client_secret = os.environ.get("REDDIT_CLIENT_SECRET"),
    user_agent = "NAME_OF_YOUR_BOT",
)

username = "REDDIT_USERNAME_TO_TRACK"

latest_post_id = None

def handle_new_post(post):
    global latest_post_id

    title = post.title
    url = post.url
    text = post.selftext
    subreddit = post.subreddit.display_name

    message = "YOUR_FORMATTED_MESSAGE"

    app.client.chat_postMessage(channel=channel_id, text=message)

    latest_post_id = post.id

# COMMENT THIS OUT TO POST THE MOST RECENT ON RUN
# Fetch the most recent post by the specified user before entering the loop
post_iterator = reddit.redditor(username).new(limit=1)
for post in post_iterator:
    latest_post_id = post.id
    break  # Exit the loop after fetching the first post without posting it

# Continuously check for new posts
while True:
    try:
        # Fetch the newest post by the specified user
        post_iterator = reddit.redditor(username).new(limit=1)
        for post in post_iterator:
            if post.id != latest_post_id:
                handle_new_post(post)
                sleep(10)
                break  # Exit the loop after processing the first post
    except Exception as e:
        print(f"Error occurred: {e}")
    sleep(10)

if __name__ == "__main__":
    app.start(port = int(os.environ.get("PORT", YOUR_DESIRED_PORT)))
