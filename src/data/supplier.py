from datetime import datetime, timedelta
import random
import json
import os

def load_supplier_updates(inventory_df, output_dir="cach/supplier"):

    today = datetime.now()
    today_str = today.strftime("%Y-%m-%d")
    updates = []

    for _, row in inventory_df.iterrows():
        if row["Units Ordered"] > 0:
            category = row["Category"]
            region = row["Region"]
            product_id = row["Product ID"]
            store_id = row["Store ID"]
            units_ordered = row["Units Ordered"]
            order_date = today - timedelta(days=random.randint(0, 3))
            order_date_str = order_date.strftime("%Y-%m-%d")

            is_delayed = random.choice([True, False])
            delay_days = random.randint(1, 5) if is_delayed else 0
            status = f"delayed by {delay_days} days" if delay_days > 0 else "on schedule"

            text = (
                f"Supplier for {category}: {status} for {units_ordered} units of {product_id} "
                f"ordered on {order_date_str} for Store {store_id} in {region}."
            )
            meta = {
                "source": "supplier", "category": category, "region": region,
                "product_id": product_id, "store_id": store_id, "date_ordered": order_date_str,
                "delay_days": delay_days
            }
            updates.append({"text": text, "metadata": meta})

    if len(updates) > 10:
        updates = random.sample(updates, 10)

    texts = [update["text"] for update in updates]
    metadata = [update["metadata"] for update in updates]

    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, f"supplier_{today_str}.json")
    with open(output_file, "w") as f:
        json.dump(updates, f, indent=4)

    return texts, metadata