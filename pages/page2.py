import os
import streamlit as st
import pandas as pd

# Load dummy data
@st.cache_data
def load_data():
    return pd.read_csv("luxury_items.csv")

# Function to check if the image path is valid (for local images)
def is_valid_image_path(image_path):
    return os.path.exists(image_path)

def main():
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
        st.button("All Categories")
    with col4:
        st.button("Account")

    # Get search query or category from session state
    search_query = st.session_state.get("search_query", "")
    category = st.session_state.get("category", "")

    if search_query:
        st.subheader(f"Search Results for '{search_query}'")
    elif category:
        st.subheader(f"Results for category: {category}")
    else:
        st.subheader("No search query or category provided.")

    data = load_data()

    # Filter data based on search query or category
    if search_query:
        filtered_data = data[data['name'].str.contains(search_query, case=False) | 
                             data['category'].str.contains(search_query, case=False)]
    elif category:
        filtered_data = data[data['category'] == category]
    else:
        filtered_data = data

    if filtered_data.empty:
        st.write("No results found.")
    else:
        # Display filtered recommendations
        cols = st.columns(3)
        for i, row in filtered_data.iterrows():
            with cols[i % 3]:
                # Check if the image file exists locally or fall back to placeholder
                image_url = row['image_url'] if is_valid_image_path(row['image_url']) else f"https://via.placeholder.com/200x150.png?text={row['name']}"
                
                st.image(image_url, use_column_width=True)
                st.markdown(f"""
                **{row['category']}**  
                {row['name']}  
                Price: ${row['price']:,.2f}
                """)
                if st.button(f"View Details", key=f"view_details_{i}"):
                    st.session_state.selected_item = row.to_dict()
                    st.switch_page("pages/item_details.py")

    # Clear session state after displaying results
    if 'search_query' in st.session_state:
        del st.session_state['search_query']
    if 'category' in st.session_state:
        del st.session_state['category']

if __name__ == "__main__":
    main()
