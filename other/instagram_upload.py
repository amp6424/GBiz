import requests

def upload_photo(image_url, caption):
    USER_ID = ''  # Replace with your Instagram user ID
    ACCESS_TOKEN = ''  # Replace with your valid access token
    
    # Step 1: Upload the image
    media_url = f'https://graph.instagram.com/{USER_ID}/media'
    media_params = {
        'image_url': image_url,  # Publicly accessible image URL
        'caption': caption,
        'access_token': ACCESS_TOKEN
    }
    
    upload_response = requests.post(media_url, params=media_params)
    media_id = upload_response.json().get('id')
    
    if not media_id:
        return {'error': 'Image upload failed', 'details': upload_response.json()}

    # Step 2: Publish the uploaded media
    publish_url = f'https://graph.instagram.com/{USER_ID}/media_publish'
    publish_params = {
        'creation_id': media_id,
        'access_token': ACCESS_TOKEN
    }
    
    publish_response = requests.post(publish_url, params=publish_params)
    return publish_response.json()

if __name__ == '__main__':
    image_url = ''# Publicly accessible image URL
    caption = 'AI Generated Graphics!'
    
    upload_response = upload_photo(image_url, caption)
    print(upload_response)
