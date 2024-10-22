import requests

# Replace these with your actual values
ACCESS_TOKEN =  ''  # Replace with your valid access token
INSTAGRAM_ACCOUNT_ID = ''  # Replace with your Instagram account ID
BASE_URL = 'https://graph.facebook.com/v17.0'

def get_instagram_insights(metric, period='day'):
    """
    Fetch insights for the specified Instagram account and metric.
    :param metric: The insight metric (e.g., 'impressions', 'reach', 'profile_views').
    :param period: The period for insights ('day', 'week', 'month', 'lifetime'). Default is 'day'.
    :return: JSON response with insights data.
    """
    url = f'{BASE_URL}/{INSTAGRAM_ACCOUNT_ID}/insights'
    params = {
        'metric': metric,  # The type of insight metric
        'period': period,  # The period (day, week, etc.)
        'access_token': ACCESS_TOKEN,  # Access token for authorization
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        return {'error': response.json()}

def get_followers_count():
    """
    Fetches the current follower count for the Instagram account.
    """
    url = f'{BASE_URL}/{INSTAGRAM_ACCOUNT_ID}'
    params = {
        'fields': 'followers_count',
        'access_token': ACCESS_TOKEN,
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        return {'error': response.json()}

if __name__ == '__main__':
    # Example usage to get different Instagram insights
    
    # Get follower count
    followers_data = get_followers_count()
    print(f"Followers Count: {followers_data.get('followers_count', 'Error retrieving data')}")

    # Get reach insights for the day
    reach_data = get_instagram_insights(metric='reach')
    print(f"Reach Insights: {reach_data}")

    # Get impressions insights for the day
    impressions_data = get_instagram_insights(metric='impressions')
    print(f"Impressions Insights: {impressions_data}")
