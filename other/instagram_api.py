import requests

# Replace with your access token and user ID
USER_ID = ''  # Replace with your Instagram user ID
ACCESS_TOKEN = '' # Replace with your Instagram access token

def get_user_media():
    url = f'https://graph.instagram.com/{USER_ID}/media?fields=id,caption,media_type,media_url,timestamp&access_token={ACCESS_TOKEN}'
    response = requests.get(url)
    return response.json()

if __name__ == '__main__':
    media_data = get_user_media()
    print(media_data)
