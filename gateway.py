#!/usr/bin/python3
#
# Gateway from pinboard.in to Mastodon

# Fill in your auth details here (TODO move to an "env" file)

# go to https://mstdn.social/settings/applications, click on your app, and
# paste the "Your access token" field here
access_token = "B...............omitted.....................x"

# The Pinboard feed to gateway from
feed_url = "https://feeds.pinboard.in/rss/u:jm/"

instance = "https://mstdn.social"

# ------------------

import feedparser
import sqlite3
import re
from datetime import datetime, timedelta
from mastodon import Mastodon

mastodon = Mastodon(
        access_token=access_token,
        api_base_url=instance
     )

# Parse the RSS feed
feed = feedparser.parse(feed_url)

one_week_ago = datetime.now() - timedelta(weeks=1)

# Connect to the SQLite database
conn = sqlite3.connect('rss_feed_tracker.db')
c = conn.cursor()

# Create a table to store processed items if it doesn't exist
c.execute('''CREATE TABLE IF NOT EXISTS processed_items
             (link TEXT PRIMARY KEY)''')

# Loop through each entry in the feed
for entry in reversed(feed.entries):
    # Extract the title, link, and description
    title = entry.title
    link = entry.link
    description = entry.description

    # strip HTML tags
    description = re.sub(r'</?blockquote>', '\"', description)
    description = re.sub(r'</?[A-Za-z]*>', '', description)

    # Check if the item has already been processed
    c.execute('SELECT * FROM processed_items WHERE link = ?', (link,))
    date = datetime(*entry.updated_parsed[:6])
    if c.fetchone() is None and date > one_week_ago:

        # Print the extracted information
        print(f"Title: {title}  Link: {link}")

        extralen = len(title) + len(link) + 9

        if len(description) > 499-extralen:
            description = description[:498-extralen] + " [\u2026]"

        body = f"{title} \u2014 {description}\n\n{link}"
        response = mastodon.status_post(body)

        # Check the response status code
        if response.id > 0:
            print(f"Successfully posted: {body}")

            # Mark the item as processed
            c.execute('INSERT INTO processed_items (link) VALUES (?)', (link,))
            conn.commit()

        else:
            print(f"Failed to post: {body}. Status code: {response}")
            raise(Exception(f"Error: {response}"))

conn.close()

