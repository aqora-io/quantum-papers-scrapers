import requests
import logging

from type import Paper

class PapersPoster:
    def __init__(self, aqora_host: str , forum_slug: str):
        self.aqora_host = aqora_host
        self.forum_slug = forum_slug
        self.session = requests.Session()

    def login_user(self, username: str, password: str): 
        login_query = {
            "query": f"""mutation {{
                loginUser(input:{{usernameOrEmail: "{username}", password: "{password}"}}) {{
                    node {{ id }}
                }}
            }}"""
        }

        headers = {'Content-Type': 'application/json', "Authorization": f"Bearer {self.aqora_host}/graphql"}
        response = self.session.post(f"{self.aqora_host}/graphql", json=login_query, headers=headers)

        if response.status_code != 200 or 'x-access-token' not in response.headers:
            logging.error("Login failed. Please check your credentials.")
            return

        bearer_token = response.headers.get('x-access-token')
        self.session.headers.update({
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {bearer_token}'
        })

    def get_story_titles(self) -> tuple[list[str], str]:
        get_latest_topics_query = {
            "query": f"""query {{
                forumBySlug(slug: "{self.forum_slug}") {{
                    id
                    topics(order: NEWEST, last: 50) {{
                        nodes {{ title }}
                    }}
                }}
            }}""", 
        }

        response = self.session.post(f"{self.aqora_host}/graphql", json=get_latest_topics_query)
        titles = []

        if response.status_code != 200:
            logging.error("Failed to fetch story titles.")
            return (titles, "")

        try:
            for node in response.json()["data"]["forumBySlug"]["topics"]["nodes"]:
                titles.append(node["title"])
        except KeyError:
            logging.error("Unexpected response structure while fetching titles.")

        return (titles, response.json()["data"]["forumBySlug"]["id"])

    def post_story(self, story_info: Paper):
        url = story_info['link']
        description = story_info['description']
        title = story_info["title"]

        titles, forum_id = self.get_story_titles()

        post_story_mutation = {
            "query": """mutation createTopic($forumId: ID!, $input: CreateTopicInput!) {
                createTopic(forumId: $forumId, input: $input) {
                    node { id }
                }
            }""",
            "variables": {
                "forumId": forum_id,
                "input": {
                    "title": title,
                    "description": description,
                    "url": url
                }
            }
        } 
        if title not in titles:
            response = self.session.post(f"{self.aqora_host}/graphql", json=post_story_mutation)
            if response.status_code == 200:
                logging.info(f"Posted story: {url}")
            else:
                logging.error(f"Failed to post story: {url}. Status Code: {response.status_code}")

