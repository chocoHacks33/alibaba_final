access_token = "EAAQutZAZAjJSQBO0jWM4T1vrIaYDRKIhWn8XYBX35Eji9mmyKk64lI2il0IkX4LyBUVMxI8ZALffM6NYqMQfhEhdekzMklZAYxjObJ7GrpDFbG4XfKEQjrts13l7SF1By9hblFZCJzQQzhuTZBZB0okc942af1LkB6FB5gx1Soh66TZAHLoWpi5eFuOeMFAeCqrMcFim0dBm"
token2 = "EAAQutZAZAjJSQBO5P66zhOZCeAm4wzNTjJ6UZB1oYHa9gcUsIu2sNaALpeXEdfq8R1czHZBkTWQ6ICnyLksZCWwWiu7ZBU7REIYDBZCI1IcQwVs7dvrToGLfmumCZAaTKBZCM9UEE0i9ZCozLJK7UdEyaVtaZB2qZCteHZATKZAGBNGAEg9kbY9HUPosymnvLaudvzZCsoTz8S4308XrDilUfiqwI60t4I6z4gx6o7RnmMEZD"
ad_account_id = "1206564054356643"
ad_account_id2 = "1040062771368100"
campaign_id = "120219014366060139"
campaign_id2 = "120221074708930718"
ad_set_id = "120219019911590139"
ad_set_id2 = "120221075121460718"
page_id = "625715383955925"
video_id = "3103055599872024"
video_id2 = "650795404441432"
image_hash = "a2f1b1fa41b4e60cf6a6f5f3d92f5589"
image_hash2 = "a2f1b1fa41b4e60cf6a6f5f3d92f5589"
website_link="https://www.facebook.com/profile.php?id=61575135659852"
ad_creative_id = "2591675034370463"
ad_creative_id2 = "1430636841651349"
ad_id="120221077389610718"

import requests
import json

def get_demographics():
    api=f"https://graph.facebook.com/v19.0/search?type=adTargetingCategory&class=demographics&access_token={access_token}"
    response = requests.get(api)
    if response.status_code == 200:
        data = response.json()
        # Pretty print the JSON response
        print(json.dumps(data, indent=4))
        return data
    else:
        print(f"Error: {response.status_code}")
        return None

def get_fb_page_id():
    # Endpoint to get Facebook Pages the user manages
    url = f"https://graph.facebook.com/v19.0/me/accounts"

    # Send the GET request
    response = requests.get(url, params={"access_token": token2})

    # Handle the response
    if response.status_code == 200:
        data = response.json()
        print("✅ Pages connected to this access token:")
        for page in data.get("data", []):
            print(f"📄 Page Name: {page['name']}")
            print(f"🔑 Page ID: {page['id']}")
            print(f"🔓 Page Token: {page['access_token']}\n")
    else:
        print(f"❌ Error: {response.status_code}")
        print(response.text)

def create_campaign():
    # API endpoint
    url = f"https://graph.facebook.com/v19.0/act_{ad_account_id2}/campaigns"

    # Campaign payload
    payload = {
        "name": "Test Campaign",
        "objective": "OUTCOME_AWARENESS",
        "status": "PAUSED",
        "special_ad_categories": [],
        "access_token": token2
    }

    # Make the POST request
    response = requests.post(url, json=payload)

    # Handle the response
    if response.status_code == 200:
        data = response.json()
        campaign_id2 = data.get("id")
        print(f"✅ Campaign created successfully. Campaign ID: {campaign_id}")
    else:
        print(f"❌ Error: {response.status_code}")
        print(response.text)

def create_ad_set():
    # API endpoint
    url = f"https://graph.facebook.com/v19.0/act_{ad_account_id2}/adsets"

    # Payload to create Ad Set
    payload = {
        "name": "Test Ad Set",
        "campaign_id": campaign_id2,
        "daily_budget": "1000",  # in minor units (i.e., 1000 = $10/day)
        "billing_event": "IMPRESSIONS",
        "optimization_goal": "IMPRESSIONS",
        "targeting": {
            "geo_locations": {"countries": ["US"]},
            "age_min": 18,
            "age_max": 35,
            "interests": [
                {"id": "6003139266461", "name": "Artificial Intelligence"}
            ]
        },
        "start_time": "2025-04-10T00:00:00-0700",
        "end_time": "2025-04-17T00:00:00-0700",
        "status": "PAUSED",
        "bid_strategy": "LOWEST_COST_WITHOUT_CAP",
        "access_token": token2
    }

    # Make the POST request
    response = requests.post(url, json=payload)

    # Handle the response
    if response.status_code == 200:
        data = response.json()
        adset_id = data.get("id")
        print(f"✅ Ad Set created successfully. Ad Set ID: {adset_id}")
    else:
        print(f"❌ Error: {response.status_code}")
        print(response.text)

def upload_facebook_ads(video_path):
    # API endpoint
    url = f"https://graph.facebook.com/v19.0/act_{ad_account_id2}/advideos"

    # Upload the video
    with open(video_path, "rb") as video_file:
        files = {
            "source": video_file
        }
        payload = {
            "access_token": token2,
            "name": "My Test Ad Video",
            "description": "Video for use in a test ad creative"
        }
        response = requests.post(url, files=files, data=payload)

    # Handle the response
    if response.status_code == 200:
        data = response.json()
        video_id = data.get("id")
        print(f"✅ Video uploaded successfully.")
        print(f"🎬 video_id: {video_id}")
    else:
        print(f"❌ Upload failed: {response.status_code}")
        print(response.text)

def upload_ad_thumbnail(thumbnail_path):
    # API endpoint for image upload
    url = f"https://graph.facebook.com/v19.0/act_{ad_account_id2}/adimages"

    # Upload image file
    with open(thumbnail_path, "rb") as image_file:
        files = {
            "filename": image_file
        }
        payload = {
            "access_token": token2
        }
        response = requests.post(url, files=files, data=payload)

    # Handle the response
    if response.status_code == 200:
        data = response.json()
        images = data.get("images", {})
        first_image = next(iter(images.values()))
        image_hash = first_image.get("hash")
        print(f"✅ Thumbnail uploaded successfully.")
        print(f"📦 image_hash: {image_hash2}")
    else:
        print(f"❌ Upload failed: {response.status_code}")
        print(response.text)


def upload_ad_creative():
    url = f"https://graph.facebook.com/v19.0/act_{ad_account_id2}/adcreatives"

    payload = {
        "name": "Video Ad Creative",
        "object_story_spec": {
            "page_id": page_id,
            "video_data": {
                "video_id": video_id2,
                "image_hash": image_hash2,
                "title": "Test AI Product Demo",
                "message": "Check out how we automate testing with AI.",
                "call_to_action": {
                    "type": "LEARN_MORE",
                    "value": {
                        "link": f"{website_link}",
                    }
                }
            }
        },
        "access_token": token2
    }

    response = requests.post(url, json=payload)

    if response.status_code == 200:
        creative_id = response.json().get("id")
        print(f"✅ Ad Creative created successfully. ID: {creative_id}")
    else:
        print(f"❌ Failed to create creative: {response.status_code}")
        print(response.text)

def create_paused_ad():
    # API endpoint
    url = f"https://graph.facebook.com/v19.0/act_{ad_account_id2}/ads"

    # Ad payload
    payload = {
        "name": "Test Ad",
        "adset_id": ad_set_id2,
        "creative": {
            "creative_id": ad_creative_id2
        },
        "status": "PAUSED",
        "access_token": token2
    }

    # Send the request
    response = requests.post(url, json=payload)

    # Handle response
    if response.status_code == 200:
        ad_id = response.json().get("id")
        print(f"✅ Ad created successfully. Ad ID: {ad_id}")
    else:
        print(f"❌ Failed to create ad. Status Code: {response.status_code}")
        print(response.text)



