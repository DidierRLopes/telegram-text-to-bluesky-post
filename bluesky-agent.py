from atproto import Client, client_utils
import os
from dotenv import load_dotenv


def main():
    load_dotenv()
    
    client = Client()
    profile = client.login(
        os.getenv('BLUESKY_HANDLE'),
        os.getenv('BLUESKY_PASSWORD')
    )
    print('Welcome,', profile.display_name)

    text = client_utils.TextBuilder().text('Hello World from ').link('Python SDK', 'https://atproto.blue')
    post = client.send_post(text)
    client.like(post.uri, post.cid)


if __name__ == '__main__':
    main()
