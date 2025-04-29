import streamlit as st
from src.data.inventory import load_inventory_data
from src.data.supplier import load_supplier_updates
from src.data.weather import load_weather_data
from src.data.news import load_news_data
from src.rag.vector_store import FAISSVectorStore
from src.rag.pipeline import process_query

st.set_page_config(page_title="SupplyChainAI", page_icon="📦", layout="wide")

st.markdown("""
    <style>
    .main {background-color: #FF8C00;}
    .stTextInput > div > div > input {border-radius: 10px; padding: 10px; background-color: #FFFFFF; color: #333333;}
    .stButton > button {border-radius: 10px; background-color: #4CAF50; color: white;}
    .stButton > button:hover {background-color: #45a049;}
    .sidebar .sidebar-content {background-color: #e0e0e0;}
    .stExpander {background-color: #FFFFFF; border-radius: 10px;}
    </style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.header("SupplyChainAI Settings")
    st.markdown("Configure your settings below.")

    show_data_sources = st.checkbox("Show Data Sources", value=False)
    st.markdown("---")

    categories = ["Groceries", "Toys", "Electronics", "Furniture", "Clothing"]
    stores = [f"S00{i}" for i in range(1, 6)]
    regions = ["North", "South", "East", "West"]
    selected_category = st.selectbox("Select Category", [""] + categories, help="Choose a product category.")
    selected_store = st.selectbox("Select Store", [""] + stores)
    selected_region = st.selectbox("Select Region", [""] + regions)
    
    if st.button("Generate Query"):
        if selected_category and selected_store and selected_region:
            query_default = f"What are the risks on {selected_category} in Store {selected_store} in the {selected_region} region?"
            st.session_state.query = query_default
        else:
            st.warning("Please select a category, store, and region.")

    st.markdown("---")

st.title("SupplyChainAI 📦")
st.markdown("Analyze supply chain risks in real-time with AI-powered insights.", help="Enter a query or use the sidebar to generate one.")

with st.spinner("Loading supply chain data..."):
    inventory_df, inv_texts, inv_metadata = load_inventory_data()
    supplier_texts, supplier_metadata = load_supplier_updates(inventory_df)
    weather_texts, weather_metadata = load_weather_data()
    news_texts, news_metadata = load_news_data()

    all_texts = inv_texts + supplier_texts + weather_texts + news_texts
    all_metadata = inv_metadata + supplier_metadata + weather_metadata + news_metadata

    vector_store = FAISSVectorStore().from_texts(all_texts, all_metadata)
st.success("Data loaded successfully!")

col1, col2 = st.columns([3, 1])
with col1:
    if "query" not in st.session_state:
        st.session_state.query = ""
    query = st.text_input("Enter your query:", 
                          value=st.session_state.query, 
                          key="query_input",
                          placeholder="e.g., 'What are the risks on Electronics in Store S001?'")
with col2:
    st.write("") 
    if st.button("Clear", key="clear_button"):
        st.session_state.query = ""
        st.rerun()

if query:
    with st.spinner("Analyzing risks..."):
        response = process_query(query, vector_store, inventory_df)
    st.markdown("### Response")
    st.markdown(response, unsafe_allow_html=True)

    if "history" not in st.session_state:
        st.session_state.history = []
    st.session_state.history.append({"query": query, "response": response})
    with st.expander("Query History"):
        for i, entry in enumerate(reversed(st.session_state.history[-5:]), 1):
            st.write(f"**Query {i}:** {entry['query']}")
            st.write(f"**Response:** {entry['response']}")
            st.markdown("---")

if show_data_sources:
    with st.expander("View Data Sources", expanded=False):
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Inventory")
            st.dataframe(inventory_df.head(), use_container_width=True)
            st.subheader("Weather")
            for text in weather_texts:
                st.write(f"- {text}")
        with col2:
            st.subheader("Supplier Updates")
            for text in supplier_texts:
                st.write(f"- {text}")
            st.subheader("News")
            for text in news_texts:
                st.write(f"- {text}")

st.markdown("---")