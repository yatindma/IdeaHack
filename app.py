import streamlit as st
import pandas as pd

# Load dummy data
@st.cache_data
def load_data():
    return pd.read_csv("luxury_items.csv")

def main():
    # Set page config to wide layout without a sidebar
    st.set_page_config(layout="wide")

    # Custom CSS to hide the sidebar
    hide_streamlit_style = """
    <style>
    /* Hide the sidebar */
    [data-testid="stSidebar"] {
        display: none;
    }
    </style>
    """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)

    # Custom CSS for buttons and input field styling
    st.markdown("""
    <style>
    .stButton>button {
        background-color: #D81B60;
        color: white;
        border-radius: 20px;
    }
    .stTextInput>div>div>input {
        background-color: #F8BBD0;
    }
    </style>
    """, unsafe_allow_html=True)

    # Header
    col1, col2, col3, col4 = st.columns([1, 4, 1, 1])
    with col1:
        st.image("logo.png", width=150)
    with col2:
        search_query = st.text_input("Search", key="search_input", label_visibility="collapsed")
    with col3:
        st.button("👤 Buyer")

    # If user enters a search query and presses enter
    if search_query:
        st.session_state.search_query = search_query
        st.switch_page("pages/page2.py")

    # Category buttons
    categories = ["Real Estate", "Stocks", "Paintings", "Gold", "Cars", "Watches", "Private Equity", "Jewellery"]
    cols = st.columns(len(categories))
    for i, category in enumerate(categories):
        with cols[i]:
            if st.button(category):
                st.session_state.category = category
                st.switch_page("pages/page2.py")

    # Recommendations
    st.subheader("Recommendations")
    data = load_data()

    # # Display some recommendations
    # cols = st.columns(3)
    # for i, row in data.iterrows():
    #     with cols[i % 3]:
    #         st.image(f"https://via.placeholder.com/200x150.png?text={row['name']}", use_column_width=True)
    #         st.markdown(f"""
    #         **{row['category']}**  
    #         {row['name']}  
    #         Price: ${row['price']:,.2f}
    #         """)
    import os

    # Function to check if the image path is valid (for local images)
    def is_valid_image_path(image_path):
        return os.path.exists(image_path)

    # Display some recommendations
    cols = st.columns(3)
    for i, row in data.iterrows():
        with cols[i % 3]:
            # Check if the image file exists locally
            if pd.notna(row['image_url']) and row['image_url'] != '' and is_valid_image_path(row['image_url']):
                image_url = row['image_url']  # Local image path
            else:
                # Use a placeholder if the image is missing
                image_url = f"https://via.placeholder.com/200x150.png?text={row['name']}"

            st.image(image_url, use_column_width=True)
            st.markdown(f"""
            **{row['category']}**  
            {row['name']}  
            Price: ${row['price']:,.2f}
            """)



if __name__ == "__main__":
    main()
