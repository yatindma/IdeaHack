import streamlit as st
import pandas as pd
import os

st.set_page_config(layout="wide", page_title="Seller Dashboard")

# Function to load data from all_items.csv
def load_all_items():
    if os.path.exists('all_items.csv'):
        return pd.read_csv('all_items.csv')
    return pd.DataFrame(columns=['item_id', 'name', 'category', 'image_url', 'listed'])

# Function to check for messages (from message.csv)
def check_messages(item_name):
    if os.path.exists('message.csv'):
        messages = pd.read_csv('message.csv')
        if item_name in messages['Product Name'].values:
            return True
    return False

# Main function for the seller's dashboard page
def main():
    # Custom CSS to enforce light theme and button styles with proper alignment
    st.markdown("""
    <style>
    body {
        background-color: #ffffff !important;
        color: #000000 !important;
    }
    .stButton>button {
        background-color: #D81B60 !important;
        color: white !important;
        border-radius: 20px !important;
        margin-top: 10px !important;
    }
    .stTextInput>div>div>input {
        background-color: #F8BBD0 !important;
        color: black !important;
    }
    h1, h2, h3, h4, h5, h6, p, label, span, .stMarkdown {
        color: black !important;  /* Ensure all text is black */
    }
    .item-details {
        background-color: #f0f0f0 !important;
        padding: 20px !important;
        border-radius: 10px !important;
        margin-top: 20px !important;
    }
    /* Override the Streamlit dark mode detection */
    [data-testid="stAppViewContainer"] {
        background-color: white !important;
    }
    [data-testid="stMarkdownContainer"] {
        color: black !important;
    }
    header, footer, .reportview-container .main {
        background-color: white !important;
        color: black !important;
    }
    </style>

    """, unsafe_allow_html=True)

    # Header section with logo and Messages button
    col1, col2, col3 = st.columns([1, 3, 1])  # Adjust column ratios
    with col1:
        st.image("logo.png", width=100)  # Add logo to the left of the search bar
    with col2:
        search_query = st.text_input("Search for an item", value="", label_visibility="collapsed")
    with col3:
        if st.button("Messages"):
            st.switch_page("pages/messages.py")

    st.write("Manage your items and listings")

    # Load items from all_items.csv
    items_df = load_all_items()

    # Filter based on search query
    if search_query:
        filtered_items = items_df[items_df['name'].str.contains(search_query, case=False)]
    else:
        filtered_items = items_df

    # Split items into listed and not listed
    listed_items = filtered_items[filtered_items['listed'] == True]
    not_listed_items = filtered_items[filtered_items['listed'] == False]

    # Display Listed items
    st.markdown('<div class="section-header">Listed Items</div>', unsafe_allow_html=True)
    if not listed_items.empty:
        cols = st.columns(3)  # Create 3 columns for tiles
        for index, row in listed_items.iterrows():
            col = cols[index % 3]  # Distribute items evenly across columns
            with col:
                with st.container():
                    st.markdown('<div class="item-box">', unsafe_allow_html=True)
                    st.markdown(f"### {row['name']}")
                    
                    # Check if the image URL is available and valid
                    if pd.notna(row['image_url']) and row['image_url'] != "":
                        image_url = row['image_url']  # Use image URL from the CSV
                    else:
                        image_url = f"https://via.placeholder.com/200x200.png?text={row['name']}"  # Use placeholder

                    # Display the image with fixed width and ensure centering using Streamlit
                    st.image(image_url, width=150, use_column_width=False)

                    st.markdown(f"**Category:** {row['category']}")

                    # Show notification if there's a message for this item
                    if check_messages(row['name']):
                        st.markdown(f"**🔔 You have messages regarding this item!** ")

                    # Center the button under the image
                    if st.button(f"List item: {row['name']}", key=f"list_button_{row['item_id']}"):
                        st.session_state['selected_item_id'] = str(row['item_id'])
                        st.switch_page("pages/1_List_Item.py")
                    st.markdown('</div>', unsafe_allow_html=True)  # Close item-box div
                st.markdown("---")
    else:
        st.write("No listed items found.")

    # Display Not Listed items
    st.markdown('<div class="section-header">Not Listed Items</div>', unsafe_allow_html=True)
    if not not_listed_items.empty:
        cols = st.columns(3)  # Create 3 columns for tiles
        for index, row in not_listed_items.iterrows():
            col = cols[index % 3]  # Distribute items evenly across columns
            with col:
                with st.container():
                    st.markdown('<div class="item-box">', unsafe_allow_html=True)
                    st.markdown(f"### {row['name']}")
                    
                    # Check if the image URL is available and valid
                    if pd.notna(row['image_url']) and row['image_url'] != "":
                        image_url = row['image_url']  # Use image URL from the CSV
                    else:
                        image_url = f"https://via.placeholder.com/200x200.png?text={row['name']}"  # Use placeholder

                    # Display the image with fixed width and ensure centering using Streamlit
                    st.image(image_url, width=150, use_column_width=False)

                    st.markdown(f"**Category:** {row['category']}")

                    # Show notification if there's a message for this item
                    if check_messages(row['name']):
                        st.markdown(f"**🔔 You have messages regarding this item!** ")

                    # Center the button under the image
                    if st.button(f"List item: {row['name']}", key=f"list_button_{row['item_id']}"):
                        st.session_state['selected_item_id'] = str(row['item_id'])
                        st.switch_page("pages/1_List_Item.py")
                    st.markdown('</div>', unsafe_allow_html=True)  # Close item-box div
                st.markdown("---")
    else:
        st.write("No unlisted items found.")

if __name__ == "__main__":
    main()
