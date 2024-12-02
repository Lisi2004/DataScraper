import streamlit as st
import requests

st.title("Marketplace Scraper")

supported_cities = ["New York", "Los Angeles", "Chicago", "Houston"]
city = st.selectbox("City", supported_cities, 0)
query = st.text_input("Query", "Laptop")
max_price = st.text_input("Max Price", "500")

submit = st.button("Submit")

if submit:
    try:
        max_price = max_price.replace(",", "")
        response = requests.get(f"http://127.0.0.1:8000/crawl_facebook_marketplace?city={city}&query={query}&max_price={max_price}")
        data = response.json()
        st.write(f"Found {len(data)} results!")
        for item in data:
            st.write(f"Title: {item['title']}, Price: {item['price']}")
    except Exception as e:
        st.error("An error occurred while fetching data.")
