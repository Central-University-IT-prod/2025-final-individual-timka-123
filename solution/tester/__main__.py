import json

import requests

BASE_URL = "http://localhost:8080"

print("Starting test engine...", "Run create advertiser endpoint", sep="\n")

adv_data = json.load(open("tester/data/advertiser.json"))
client_data = json.load(open("tester/data/clients.json"))
campaigns_data = json.load(open("tester/data/campaigns.json"))
scores = json.load(open("tester/data/mls.json"))

response = requests.post(
    url=f"{BASE_URL}/advertisers/bulk",
    json=adv_data
)
if response.status_code != 201:
    print("Request to register advertiser has not 201 status code")


response = requests.post(
    url=f"{BASE_URL}/clients/bulk",
    json=client_data
)

if response.status_code != 201:
    print("Request to register clients has not 201 status code")


print("\nStarting registering campaign data")
for campaign in campaigns_data:
    response = requests.post(
        url=f"{BASE_URL}/advertisers/{campaign['advertiser_id']}/campaigns",
        json=campaign['campaign_data']
    )
    if response.status_code != 201:
        print(f"Request for create campaign failed with {response.status_code} status code and response: {response.text}")

    
print("Finished.\n\nStarting applying ML scores")

for score in scores:
    try:
        response = requests.post(
            url=f"{BASE_URL}/ml-scores",
            json=score
        )
        if response.status_code != 200:
            print(f"Request for edit ml score failed with status {response.status_code} and response: {response.text}")
    except Exception as e:
        print(f"Request for apply ml score failed with exception: {e}")

print(f"Finished testing on public tests.")
