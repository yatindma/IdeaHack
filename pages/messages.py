import streamlit as st
import pandas as pd
import os

st.set_page_config(layout="wide", page_title="Messages")

# Function to load messages from message.csv
def load_messages():
    if os.path.exists('message.csv'):
        return pd.read_csv('message.csv')
    return pd.DataFrame(columns=['Product Name', 'Message'])

# Main function for the messages page
def main():
    st.header("Messages")

    # Load messages
    messages_df = load_messages()

    if messages_df.empty:
        st.write("No messages found.")
    else:
        # Display messages in a table
        st.table(messages_df)

    # Button to go back to the seller dashboard
    if st.button("Back to Dashboard"):
        st.switch_page("seller_dashboard")

if __name__ == "__main__":
    main()
