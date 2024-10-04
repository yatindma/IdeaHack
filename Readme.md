

# Luxury Marketplace Application

This is a luxury marketplace application built using Streamlit, where sellers can list items and buyers can purchase items from the marketplace.

## Setup Instructions

### 1. Virtual Environment Setup

Create a virtual environment using the following command:
```bash
python3 -m venv venv
```

Activate the virtual environment:
- On macOS/Linux:
    ```bash
    source venv/bin/activate
    ```
- On Windows:
    ```bash
    venv\Scripts\activate
    ```

### 2. Install Required Dependencies

Install the required packages using the `requirements.txt` file:
```bash
pip install -r requirements.txt
```

### 3. Running the Application

#### Seller Flow

To run the seller flow where sellers can list items from the `all_items.csv`, use the following command:
```bash
streamlit run seller_dashboard.py   
```

#### Buyer Flow

To run the buyer flow where buyers can view and purchase listed items, use the following command:
```bash
streamlit run app.py
```

---

## CSV File Structure

The application uses a CSV file (`all_items.csv`) with the following structure:

```csv
item_id,name,category,image_url,listed
1,Luxury Watch,Watches,watch.png,false
2,Patek Philippe Nautilus,Watches,watch.png,false
...
```

Items that are not yet listed will have `listed` set to `false`. Once an item is listed, the value will change to `true`.

---

## How It Works

### Seller Flow
- Sellers can view items that are not yet listed (i.e., `listed = false`) and choose to list them.
- Once listed, the status of the item will change to `true` in the CSV file.

### Buyer Flow
- Buyers can view all listed items (i.e., `listed = true`) and choose to purchase an item.
