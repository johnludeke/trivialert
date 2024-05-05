import os
import praw
from time import sleep
from slack_bolt import App

import ssl
ssl._create_default_https_context = ssl._create_unverified_context

# Initialize your app with your bot token and signing secret
app = App(
    token = os.environ.get("SLACK_BOT_TOKEN"),
    signing_secret = os.environ.get("SLACK_SIGNING_SECRET"),
)

# for testing : C06RQBBAL0P
# for trivia  : C06L12LFC0G
channel_id = "C06L12LFC0G"

# Initialize the Reddit API client
reddit = praw.Reddit(
    client_id = os.environ.get("REDDIT_CLIENT_ID"),
    client_secret = os.environ.get("REDDIT_CLIENT_SECRET"),
    user_agent = "trivialert",
)

# Specify the Reddit username to monitor
username = "Murphyspubuofi"

# Keep track of the latest post ID
latest_post_id = None

# Function to handle new posts by the specified user
def handle_new_post(post):
    global latest_post_id

    # Extract relevant information from the post
    title = post.title
    url = post.url
    text = post.selftext
    subreddit = post.subreddit.display_name

    # Compose the message to be sent to Slack
    message = f":alert: HEY <!channel> :alert:\n{username} in r/{subreddit} just posted :blobhyper:\n\n*{title}*\n{text}\n\n({url})"

    # Send the message to the specified Slack channel
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
        # Handle exceptions gracefully (e.g., rate limit exceeded)
        print(f"Error occurred: {e}")
    sleep(10)

# Launch app
if __name__ == "__main__":
    app.start(port = int(os.environ.get("PORT", 3000)))
