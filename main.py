import os
import sys
import logging
from papers_poster import PapersPoster

from scirate import scrape_scirate

def main():
    # Configure logging
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)

    if len(sys.argv) < 5:
        logging.error(
            "Usage: [python3/pthon/uv run] main.py [scraper_names/all] [username] [password] [forum_slug]"
        )
        return

    scraper_names_input = sys.argv[1]
    username = sys.argv[2]
    password = sys.argv[3]
    forum_slug = sys.argv[4]

    aqora_host = os.getenv("AQORA_HOST", "https://app-staging.aqora-internal.io")

    poster = PapersPoster(aqora_host, forum_slug)
    poster.login_user(username, password)

    # List of all scrapers and their corresponding functions
    all_scrapers = {
        "scirate": scrape_scirate,
        # Add more scrapers here as needed
    }

    scraper_names = (
        scraper_names_input.split(",")
        if scraper_names_input != "all"
        else all_scrapers.keys()
    )

    for scraper_name in scraper_names:
        scraper_function = all_scrapers.get(scraper_name)
        if scraper_function:
            stories = scraper_function()
            if len(stories) == 0:
                logging.info(f"No new stories found from {scraper_name}")
            for story in stories:
                poster.post_story(story)
        else:
            logging.error(f"Unknown scraper: {scraper_name}")


if __name__ == "__main__":
    main()
