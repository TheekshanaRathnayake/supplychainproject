from datetime import datetime
import random
import json
import os

def load_weather_data(output_dir="cach/weather"):

    today = datetime.now().strftime("%Y-%m-%d")
    regions = ["North", "South", "East", "West"]
    conditions = ["Sunny", "Rainy", "Cloudy", "Snowy"]

    updates = []
    for region in regions:
        condition = random.choice(conditions)
        text = f"Weather in {region} on {today}: {condition}."
        meta = {"source": "weather", "region": region, "date": today, "condition": condition}
        updates.append({"text": text, "metadata": meta})

    texts = [update["text"] for update in updates]
    metadata = [update["metadata"] for update in updates]

    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, f"weather_{today}.json")
    with open(output_file, "w") as f:
        json.dump(updates, f, indent=4)

    return texts, metadata