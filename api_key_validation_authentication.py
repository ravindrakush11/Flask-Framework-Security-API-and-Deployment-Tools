# pip install requests
import requests

# Replace 'your_api_key_here' with your actual Groq API key
api_key = 'your api key'
url = 'https://api.groq.com/openai/v1/models'  # Replace with a valid Groq API endpoint

# Set up the headers with your API key for authentication
headers = {
    'Authorization': f'Bearer {api_key}',
    'Content-Type': 'application/json'
}

# Make a GET request to the API endpoint
try:
    response = requests.get(url, headers=headers)
    
    # Check if the response is successful
    if response.status_code == 200:
        print("API key is valid and authenticated successfully.")
    elif response.status_code == 401:
        print("Invalid API key. Authentication failed.")
    else:
        print(f"Failed to authenticate. Status code: {response.status_code}")
        print(f"Response: {response.json()}")
except requests.exceptions.RequestException as e:
    print(f"An error occurred: {e}")
