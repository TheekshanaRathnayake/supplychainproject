from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def process_query(query, vector_store, inventory_df):
    docs = vector_store.similarity_search(query, k=5)
    context = "\n".join([doc["text"] for doc in docs])

    category = None
    store_id = None
    if "on" in query and "Store" in query:
        category = query.split("on")[1].split("in")[0].strip()
        store_id = query.split("Store")[1].split()[0].strip()

    if category and store_id:
        product_data = inventory_df[
            (inventory_df["Category"] == category) & (inventory_df["Store ID"] == store_id)
        ]
        if not product_data.empty:
            total_inventory = product_data["Inventory Level"].sum()
            total_sold = product_data["Units Sold"].sum()
            total_ordered = product_data["Units Ordered"].sum()
            avg_demand = round(product_data["Demand Forecast"].mean(), 2)
            inventory_summary = (
                f"Inventory for {category} at {store_id}: {total_inventory} total units across products, "
                f"{total_sold} sold today, {total_ordered} ordered, "
                f"Average demand forecast: {avg_demand} units/day."
            )
            context += "\n" + inventory_summary

    prompt = f"Given this context:\n{context}\n\nAnswer the query: {query}"
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=500
    )
    return response.choices[0].message.content