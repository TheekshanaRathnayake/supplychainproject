# SupplyChainAI

A real-time supply chain risk analysis tool powered by AI, using simulated inventory, supplier, weather, and news data.

## Details

- **Purpose**: Analyze supply chain risks based on category, store, and region.
- **Date**: Simulates real time data.
- **Tech**: Streamlit (UI), FAISS (vector search), OpenAI (LLM), Python.
- **UI**:  Sidebar settings and query input.

## Workflow

1. **Start**: Run `app.py` with `streamlit run app.py`.
2. **Data Loading**: Loads simulated data from inventory, supplier, weather, and news.
3. **Query**: Enter a query (e.g., "What are the risks on Electronics in Store S001?") or use the sidebar to generate one.
4. **Analysis**: FAISS retrieves relevant data; OpenAI generates a risk analysis.
5. **Output**: Displays response with inventory summary, risks, and recommendations.
6. **Extras**: View data sources or query history via expanders.

## Files

- **`app.py`**  
  Main Streamlit app. Sets up the UI (dark orange background), sidebar (category/store/region selectors), and query processing.

- **`inventory.py`**  
  Simulates inventory data (e.g., stock, sales) for 5 stores and 20 products. Saves to `cach/inventory/inventory_YYYY-MM-DD.csv`.

- **`supplier.py`**  
  Simulates supplier updates (e.g., delays) based on inventory orders. Saves to `cach/supplier/supplier_YYYY-MM-DD.json`.

- **`weather.py`**  
  Simulates weather conditions for 4 regions (North, South, East, West). Saves to `cach/weather/weather_YYYY-MM-DD.json`.

- **`news.py`**  
  Simulates news disruptions (e.g., strikes, shortages) for categories and regions. Saves to `cach/news/news_YYYY-MM-DD.json`.

- **`vector_store.py`**  
  Implements FAISS vector store to embed and search text data using `all-MiniLM-L6-v2` model.

- **`pipeline.py`**  
  Processes queries with OpenAI’s `gpt-3.5-turbo`. Summarizes inventory by category/store and generates responses.

## Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Add API key to `.env`: `OPENAI_API_KEY=your-key`
3. Run: `streamlit run app.py`
4. Open: `http://localhost:8501`
