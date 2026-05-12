import requests
import json
import boto3

url = "https://apim.laliga.com/public-service/api/v1/subscriptions/laliga-easports-2025/players/rankings"

headers = {
    "User-Agent": "Mozilla/5.0"
}

access_key = "xyz"
secret_key = "abc"

bucket_name = "barca-kings-raw-data"
s3_key = "barca-raw-data/laliga/players_stats.json"

databricks_host = "https://dbc-934e64d2-fbc7.cloud.databricks.com/"
databricks_token = "dummy"

volume_path = "/Volumes/workspace/bk_raw/laliga_raw_files/players_stats.json"

# Create S3 client
s3 = boto3.client(
    "s3",
    aws_access_key_id=access_key,
    aws_secret_access_key=secret_key,
    region_name="us-east-1"
)

all_barca_players = []
offset = 0
limit = 100

while True:
    params = {
        "limit": limit,
        "offset": offset,
        "orderField": "stat.total_goals",
        "orderType": "DESC",
        "contentLanguage": "en",
        "subscription-key": "c13c3a8e2f6b46da9c5c425cf61fab3e"
    }

    res = requests.get(url, params=params, headers=headers)
    data = res.json()

    players = data.get("player_rankings", [])
    
    # Stop when no more data
    if not players:
        break

    for p in players:
        if not isinstance(p, dict):
            continue

        # ✅ Filter FC Barcelona players
        if p.get("team", {}).get("slug") == "fc-barcelona":
            all_barca_players.append(p)

    offset += limit

json_data = json.dumps(all_barca_players, indent=4, ensure_ascii=False)


# Upload to S3
s3.put_object(
    Bucket=bucket_name,
    Key=s3_key,
    Body=json_data,
    ContentType="application/json"
)

print("✅ File uploaded to S3 successfully")

response = requests.put(
    f"{databricks_host}/api/2.0/fs/files{volume_path}",
    headers={
        "Authorization": f"Bearer {databricks_token}",
        "Content-Type": "application/octet-stream"
    },
    data=json_data.encode("utf-8")  # ✅ send as bytes
)

print(response.status_code)
print(response.text)

print("✅ File uploaded to Databricks successfully")