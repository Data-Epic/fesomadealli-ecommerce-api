import pandas as pd

try:
    df = pd.read_csv("data\ecommerce_dataset.csv")
    print("dataset read into memory successfully")
    
except FileNotFoundError:
    print("Error: 'ecommerce_dataset.csv' not found. Please check the file path.")
except Exception as e:
    print(f"An unexpected error occurred: {e}")


# CUSTOMER LOGIN TYPE COLUMN
df["Customer_Login_type"] = df["Customer_Login_type"].str.strip()


# AGING COLUMN
for index, row in df[df["Aging"].isnull()].iterrows():
    product_type = row["Product"]
    product_df = df[df["Product"] == product_type]

    try:
        mode_aging = product_df["Aging"].mode()[0]
    except IndexError:
        mode_aging = 0

    df.loc[index, "Aging"] = mode_aging


# SALES COLUMN
for index, row in df.iterrows():
    if pd.isnull(row["Sales"]):
        product_type = row["Product"]
        mode_sales = df[df["Product"] == product_type]["Sales"].mode()

        if not mode_sales.empty:
            df.loc[index, "Sales"] = mode_sales[0]
        else:
            df.loc[index, "Sales"] = df["Sales"].mode()[0]


# DISCOUNT COLUMN
df["Discount"] = df["Discount"].fillna(0.0)


# QUANTITY COLUMN
for index, row in df[df["Quantity"].isnull()].iterrows():
    customer_id = row["Customer_Id"]
    customer_df = df[df["Customer_Id"] == customer_id]

    if len(customer_df) == 1:
        product = row["Product"]
        mode_product = df[df["Product"] == product]["Quantity"].mode()
        df.loc[index, "Quantity"] = mode_product[0]

    elif len(customer_df) > 1:
        product = row["Product"]
        customer_product_df = customer_df[customer_df["Product"] == product]

        if len(customer_product_df) == 1:
            mode_product = df[df["Product"] == product]["Quantity"].mode()
            df.loc[index, "Quantity"] = mode_product[0]

        elif len(customer_product_df) > 1:
            non_nan_quantities = customer_product_df["Quantity"].dropna()
            if not non_nan_quantities.empty:
                mode_quantity = non_nan_quantities.mode()
                if not mode_quantity.empty:
                    df.loc[index, "Quantity"] = mode_quantity[0]
                else:
                    df.loc[index, "Quantity"] = df["Quantity"].mode()[0]
            else:
                df.loc[index, "Quantity"] = df["Quantity"].mode()[0]


# SHIPPING COLUMN
for index, row in df[df["Shipping_Cost"].isnull()].iterrows():
    product_type = row["Product"]
    product_df = df[df["Product"] == product_type]
    
    try:
        mode_shipping_cost = product_df["Shipping_Cost"].mode()[0]
    except IndexError:
        mode_shipping_cost = df[
            "Shipping_Cost"
        ].mean()  
        
    df.loc[index, "Shipping_Cost"] = mode_shipping_cost


# ORDER PRIORITY COLUMN
for index, row in df[df["Order_Priority"].isnull()].iterrows():
    customer_id = row["Customer_Id"]
    customer_df = df[df["Customer_Id"] == customer_id]

    if len(customer_df) == 1:
        product = row["Product"]
        mode_product = df[df["Product"] == product]["Order_Priority"].mode()

        if not mode_product.empty:
            df.loc[index, "Order_Priority"] = mode_product[0]
        else:
            df.loc[index, "Order_Priority"] = df["Order_Priority"].mode()[0]

    elif len(customer_df) > 1:
        mode_priority = customer_df["Order_Priority"].mode()
        if not mode_priority.empty:
            df.loc[index, "Order_Priority"] = mode_priority[0]
        else:
            df.loc[index, "Order_Priority"] = df["Order_Priority"].mode()[0]


df["Order_Date"] = pd.to_datetime(df["Order_Date"]).dt.date
df["Quantity"] = df["Quantity"].astype(int)

df.sort_values(by="Order_Date")

ecommerce_cleaned = df

ecommerce_cleaned.rename(
    columns={
        "Order_Date": "order_date",
        "Time": "time",
        "Aging": "aging",
        "Customer_Id": "customer_id",
        "Gender": "gender",
        "Device_Type": "device_type",
        "Customer_Login_type": "login_type",
        "Product_Category": "product_category",
        "Product": "product_name",
        "Sales": "sales",
        "Quantity": "quantity",
        "Discount": "discount",
        "Profit": "profit",
        "Shipping_Cost": "shipping_cost",
        "Order_Priority": "order_priority",
        "Payment_method": "payment_method",
    },
    inplace=True,
)

ecommerce_cleaned = ecommerce_cleaned.reset_index()

print("data cleaning successful!")
