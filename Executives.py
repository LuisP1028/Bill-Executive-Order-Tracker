import feedparser
import os
import re
from win10toast import ToastNotifier

# RSS URL and paths
rss_url = ''
orders_dir = r''
last_fetched_file = r''

# Initialize the toast notifier
toaster = ToastNotifier()

# Function to truncate strings if they're too long
def truncate_string(s, max_length):
    """Truncate a string to the max_length and append '...' if needed."""
    return s if len(s) <= max_length else s[:max_length - 3] + "..."

# Function to check the feed and notify about new entries
def check_feed():
    feed = feedparser.parse(rss_url)
    new_entries = []

    last_fetched = None
    if os.path.exists(last_fetched_file):
        with open(last_fetched_file, 'r') as f:
            last_fetched = f.read().strip()

    for entry in feed.entries[:5]:  # Only process the last 5 entries
        if entry.link != last_fetched:
            new_entries.append(entry)
        else:
            break

    if new_entries:
        for entry in new_entries:
            filename = re.sub(r'[\\/*?:"<>|]', "_", entry.title)
            filepath = os.path.join(orders_dir, f"{filename}.txt")

            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(f"Title: {entry.title}\n")
                f.write(f"Link: {entry.link}\n")
                f.write(f"Published: {entry.published}\n")

            # Truncate title and link for notification
            truncated_title = truncate_string(entry.title, 64)
            truncated_message = truncate_string(entry.link, 64)

            # Show toast notification
            toaster.show_toast(
                f"New Executive Order: {truncated_title}",
                f"Click to read more: {truncated_message}",
                duration=10  # Time in seconds
            )

        with open(last_fetched_file, 'w') as f:
            f.write(new_entries[0].link)

if __name__ == "__main__":
    check_feed()
