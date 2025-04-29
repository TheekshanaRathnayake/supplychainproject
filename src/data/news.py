from datetime import datetime, timedelta
import random
import json
import os

def load_news_data(output_dir="cach/news"):

    today = datetime.now()
    today_str = today.strftime("%Y-%m-%d")
    categories = ["Groceries", "Toys", "Electronics", "Furniture", "Clothing"]
    regions = ["North", "South", "East", "West"]
    disruptions = [
        "port strike affecting shipments",
        "severe weather disrupting logistics",
        "supplier bankruptcy reported",
        "transportation delays due to road closures",
        "labor shortage impacting warehouse operations",
        "fuel price surge increasing shipping costs",
        "customs delays holding up imports",
        "factory shutdown due to power outage",
        "cyberattack disrupting supplier systems",
        "raw material shortage affecting production"
    ]

    updates = []
    for _ in range(5):
        category = random.choice(categories)
        region = random.choice(regions)
        disruption = random.choice(disruptions)
        date = (today - timedelta(days=random.randint(0, 2))).strftime("%Y-%m-%d")
        text = f"News on {date}: {disruption} impacting {category} in {region}."
        meta = {"source": "news", "category": category, "region": region, "date": date}
        updates.append({"text": text, "metadata": meta})

    texts = [update["text"] for update in updates]
    metadata = [update["metadata"] for update in updates]

    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, f"news_{today_str}.json")
    with open(output_file, "w") as f:
        json.dump(updates, f, indent=4)

    return texts, metadata