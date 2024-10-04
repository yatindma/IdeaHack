import streamlit as st
import pandas as pd
import os

st.set_page_config(layout="wide", page_title="List Item")

# Function to load the selected item from all_items.csv
def load_item(item_id):
    if os.path.exists('all_items.csv'):
        all_items = pd.read_csv('all_items.csv')
        item = all_items[all_items['item_id'] == int(item_id)]
        if not item.empty:
            st.write(f"Loaded item from all_items.csv: {item}")
            return item.iloc[0]
        else:
            st.error("Item not found in all_items.csv")
            return None
    else:
        st.error("all_items.csv not found")
        return None

# Function to move the item from all_items.csv to luxury_items.csv
def list_item(item_id, name, category, description, price, image_url, details, hide_fields, seller_details):
    try:
        # Prepare new item details to be saved in luxury_items.csv
        new_item = pd.DataFrame([{
            'item_id': item_id,
            'name': name if 'name' not in hide_fields else '',
            'category': category if 'category' not in hide_fields else '',
            'description': description if 'description' not in hide_fields else '',
            'price': price if 'price' not in hide_fields else '',
            'image_url': image_url if 'image_url' not in hide_fields else '',
            'details': details if 'details' not in hide_fields else '',
            'hide_fields': ','.join(hide_fields),  # Store hidden fields
            'seller_details': seller_details
        }])

        # Check if luxury_items.csv exists
        if os.path.exists('luxury_items.csv'):
            luxury_items = pd.read_csv('luxury_items.csv')
        else:
            luxury_items = pd.DataFrame(columns=['item_id', 'name', 'category', 'description', 'price', 'image_url', 'details', 'hide_fields', 'seller_details'])

        # Append new item to luxury_items dataframe
        luxury_items = pd.concat([luxury_items, new_item], ignore_index=True)

        # Save the updated luxury_items.csv
        luxury_items.to_csv('luxury_items.csv', index=False)
        # Update the listed flag in all_items.csv
        if os.path.exists('all_items.csv'):
            all_items = pd.read_csv('all_items.csv')
            # Update the listed flag for the specific item
            all_items.loc[all_items['item_id'] == int(item_id), 'listed'] = True
            # Save the updated all_items.csv
            all_items.to_csv('all_items.csv', index=False)
        st.success(f"Item '{name}' successfully listed!")

    except Exception as e:
        st.error(f"Error listing item: {e}")
        st.write(f"Current working directory: {os.getcwd()}")

# Custom CSS styling to enforce light theme and apply color palette
st.markdown("""
<style>
body {
    background-color: #ffffff !important;  /* Light theme background */
    color: #000000 !important;             /* Black text */
}

/* Force button styling for all states (normal, hover, active) */
.stButton>button {
    background-color: #D81B60 !important;  /* Red button */
    color: white !important;               /* White text */
    border-radius: 20px !important;
    border: none !important;
}

/* Ensure the button stays red on hover and active states */
.stButton>button:hover {
    background-color: #C2185B !important;  /* Slightly darker red on hover */
    color: white !important;
}

.stButton>button:active {
    background-color: #B0003A !important;  /* Darker red when button is clicked */
    color: white !important;
}

/* Text input and text area styling */
.stTextInput>div>div>input, .stTextArea>div>div>textarea {
    background-color: #ffffff !important;  /* White background for inputs */
    color: black !important;               /* Black text inside inputs */
    border: 1px solid #D81B60 !important;  /* Red border */
    padding: 10px !important;
    border-radius: 10px !important;
}

/* Dropdown (select box) styling */
.stSelectbox>div>div>div {
    background-color: #ffffff !important;  /* White background for dropdown */
    color: black !important;               /* Black text for dropdown options */
    border: 1px solid #D81B60 !important;  /* Red border */
}

/* Selected dropdown item */
.stSelectbox>div>div>div:focus {
    background-color: #D81B60 !important;  /* Red background when an item is selected */
    color: white !important;               /* White text when selected */
}

/* General form fields styling */
.stSelectbox, .stTextInput, .stTextArea {
    color: black !important;
    border: 1px solid #D81B60 !important; /* Red border for input fields */
}

/* Force light theme */
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


# Get item_id from session state
item_id = st.session_state.get('selected_item_id')
if item_id is None:
    st.error("No item selected. Please go back and select an item.")
    st.stop()

# Load the selected item details
item = load_item(item_id)
if item is None:
    st.error("Item not found.")
    st.stop()

# Display the item details
st.markdown(f"### Listing Item: {item['name']}")
st.image(item['image_url'], use_column_width=True)
st.markdown(f"**Category:** {item['category']}")

# Form for the seller to add additional details
with st.form(key="list_item_form"):
    description = st.text_area("Add a description", value="")
    price = st.number_input("Set a price (€)", min_value=0.0, step=0.01)
    hide_fields = st.multiselect("Select fields to hide from the buyer", options=["name", "category", "description", "price", "image_url", "details"])

    seller_details = st.text_input("Seller details (optional)")

    submit_button = st.form_submit_button("List this item")
    if submit_button:
        list_item(
            item_id=item_id,
            name=item['name'],
            category=item['category'],
            description=description,
            price=price,
            image_url=item['image_url'],
            details=item['details'] if 'details' in item else '',
            hide_fields=hide_fields,
            seller_details=seller_details
        )
        st.balloons()
