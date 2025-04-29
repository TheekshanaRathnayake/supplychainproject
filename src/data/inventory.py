import pandas as pd
from datetime import datetime
import random
import os

def load_inventory_data(output_dir="cach/inventory"):

    today = datetime.now().strftime("%Y-%m-%d")
    stores = [f"S00{i}" for i in range(1, 6)]
    products = [f"P00{i:02d}" for i in range(1, 21)]
    categories = ["Groceries", "Toys", "Electronics", "Furniture", "Clothing"]
    regions = ["North", "South", "East", "West"]
    weather_conditions = ["Sunny", "Rainy", "Cloudy", "Snowy"]

    data = []
    for store in stores:
        for product in products:
            category = random.choice(categories)
            region = random.choice(regions)
            inventory_level = random.randint(50, 500)
            units_sold = random.randint(0, min(400, inventory_level))
            units_ordered = random.randint(0, 200)
            demand_forecast = round(random.uniform(units_sold * 0.8, units_sold * 1.2), 2)
            price = round(random.uniform(10, 100), 2)
            discount = random.choice([0, 5, 10, 15, 20])
            weather = random.choice(weather_conditions)
            holiday = random.choice([0, 1])
            competitor_price = round(price * random.uniform(0.9, 1.1), 2)
            seasonality = random.choice(["Spring", "Summer", "Autumn", "Winter"])

            data.append([
                today, store, product, category, region, inventory_level, units_sold,
                units_ordered, demand_forecast, price, discount, weather, holiday,
                competitor_price, seasonality
            ])

    columns = [
        "Date", "Store ID", "Product ID", "Category", "Region", "Inventory Level",
        "Units Sold", "Units Ordered", "Demand Forecast", "Price", "Discount",
        "Weather Condition", "Holiday/Promotion", "Competitor Pricing", "Seasonality"
    ]
    df = pd.DataFrame(data, columns=columns)

    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, f"inventory_{today}.csv")
    df.to_csv(output_file, index=False)

    texts = [
        f"Store {row['Store ID']} on {row['Date']}: {row['Inventory Level']} units of {row['Product ID']} "
        f"({row['Category']}) in {row['Region']}, {row['Units Sold']} sold, {row['Units Ordered']} ordered."
        for _, row in df.iterrows()
    ]
    metadata = [
        {"source": "inventory", "store_id": row["Store ID"], "product_id": row["Product ID"],
         "category": row["Category"], "region": row["Region"], "date": row["Date"]}
        for _, row in df.iterrows()
    ]

    return df, texts, metadata