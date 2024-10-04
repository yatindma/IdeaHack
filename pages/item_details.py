import streamlit as st
import pandas as pd
import ast
import os
import csv

# Function to parse the 'details' field, either as a dictionary or a string
def parse_details(details_str):
    try:
        return ast.literal_eval(details_str)
    except:
        return details_str

# Function to load the CSV data, handling missing fields
def load_data():
    df = pd.read_csv("luxury_items.csv")
    
    # Fill missing values with sensible defaults
    df['details'] = df['details'].apply(parse_details).fillna('')
    df['price'] = df['price'].fillna(0.0)
    df['category'] = df['category'].fillna('Unknown Category')
    df['image_url'] = df['image_url'].fillna('https://via.placeholder.com/400x300?text=No+Image')
    
    return df

# Function to display a popup message
def show_popup():
    st.markdown(
        """
        <style>
        .popup {
            position: fixed;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background-color: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 0 10px rgba(0,0,0,0.3);
            z-index: 9999;
        }
        .popup-bg {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-color: rgba(0,0,0,0.5);
            z-index: 9998;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    
    st.markdown(
        """
        <div class="popup-bg"></div>
        <div class="popup">
            <h3>Your request has been sent!</h3>
            <p>We'll get back to you soon.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

# Function to save the message to a CSV
def save_message_to_csv(product_name, message):
    filename = "message.csv"
    
    try:
        with open(filename, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            if os.stat(filename).st_size == 0:  # Write header if file is empty
                writer.writerow(['Product Name', 'Message'])
            writer.writerow([product_name, message])
        st.success(f"Message saved successfully to {filename}")
    except Exception as e:
        st.error(f"An error occurred while saving the message: {str(e)}")
        st.error(f"Current working directory: {os.getcwd()}")

# Main function for the app
def main():
    st.set_page_config(layout="wide")

    # Force the light theme
    st.markdown("""
    <style>
    body {
        background-color: #ffffff !important;
        color: #000000 !important;
    }
    .stButton>button {
        background-color: #D81B60;
        color: white;
        border-radius: 20px;
    }
    .stTextInput>div>div>input {
        background-color: #F8BBD0;
        color: black;
    }
    .item-details {
        background-color: #f0f0f0;
        padding: 20px;
        border-radius: 10px;
        margin-top: 20px;
    }
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

    col1, col2, col3, col4 = st.columns([1, 4, 1, 1])
    with col1:
        st.image("logo.png", width=150)
    with col2:
        st.text_input("Search", key="search_input", label_visibility="collapsed")
    with col3:
        st.button("All Categories")
    with col4:
        st.button("Account")

    # Load the data and print it to the app
    data = load_data()

    # Get the selected item from session state or default to the first item
    if 'selected_item' in st.session_state:
        item = st.session_state.selected_item
    else:
        item = data.iloc[0].to_dict()

    # Display item category and name
    st.markdown(f"{item['category']} > {item['name']}")

    col1, col2 = st.columns([1, 1])

    with col1:
        st.image(item['image_url'], use_column_width=True, caption=item['name'])

    with col2:
        st.markdown(f"<h2>{item['name']}</h2>", unsafe_allow_html=True)
        st.markdown(f"<h3 style='color: #D81B60;'>{item['price']:,.2f}€</h3>", unsafe_allow_html=True)
        st.markdown(f"<p>{item['description']}</p>", unsafe_allow_html=True)
        
        st.markdown("<div class='item-details'>", unsafe_allow_html=True)
        if isinstance(item['details'], dict):
            for key, value in item['details'].items():
                st.markdown(f"<p><strong>{key}:</strong> {value}</p>", unsafe_allow_html=True)
        elif isinstance(item['details'], str):
            details_list = item['details'].split(', ')
            for detail in details_list:
                parts = detail.split(': ')
                if len(parts) == 2:
                    key, value = parts
                    st.markdown(f"<p><strong>{key}:</strong> {value}</p>", unsafe_allow_html=True)
                else:
                    st.markdown(f"<p>{detail}</p>", unsafe_allow_html=True)
        else:
            st.markdown(f"<p>{item['details']}</p>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
        if st.button("Connect"):
            st.session_state.show_form = True

        if 'show_form' in st.session_state and st.session_state.show_form:
            with st.form("contact_form"):
                st.write("Contact Options")
                contact_method = st.selectbox("Preferred contact method", ["Phone", "Email", "Message"])
                message = st.text_area("Your Message")
                submitted = st.form_submit_button("Send Message")
                if submitted:
                    save_message_to_csv(item['name'], message)
                    show_popup()
                    st.success(f"Your message has been sent via {contact_method}!")
                    st.balloons()
                    st.session_state.show_form = False

if __name__ == "__main__":
    main()
