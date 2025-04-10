token = "EAAQutZAZAjJSQBO0jWM4T1vrIaYDRKIhWn8XYBX35Eji9mmyKk64lI2il0IkX4LyBUVMxI8ZALffM6NYqMQfhEhdekzMklZAYxjObJ7GrpDFbG4XfKEQjrts13l7SF1By9hblFZCJzQQzhuTZBZB0okc942af1LkB6FB5gx1Soh66TZAHLoWpi5eFuOeMFAeCqrMcFim0dBm"
campaign_id = "120219014366060139"

import requests
import json

def get_demographics():
    api=f"https://graph.facebook.com/v19.0/search?type=adTargetingCategory&class=demographics&access_token={token}"
    response = requests.get(api)
    if response.status_code == 200:
        data = response.json()
        # Pretty print the JSON response
        print(json.dumps(data, indent=4))
        return data
    else:
        print(f"Error: {response.status_code}")
        return None

if __name__ == "__main__":
    get_demographics()