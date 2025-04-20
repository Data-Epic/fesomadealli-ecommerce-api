import sys
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from clean import ecommerce_cleaned
from database.db_setup import engine, db_to_connect
from database.models import Customers, Orders, Products, Order_Items
from database.crud import session


from sqlalchemy.dialects.postgresql import insert  # type: ignore

def load_data_into_postgres(val=False):
    if val == True:
        # #Customers
        try:
            customer_df = ecommerce_cleaned[
                ["customer_id", "gender", "device_type", "login_type"]
            ]
            for index, row in customer_df.iterrows():
                insert_stmt = insert(Customers).values(
                    customer_id=row["customer_id"],
                    gender=row["gender"],
                    device_type=row["device_type"],
                    login_type=row["login_type"],
                )

                upsert_stmt = insert_stmt.on_conflict_do_update(
                    index_elements=["customer_id"],
                    set_={
                        "gender": insert_stmt.excluded.gender,
                        "device_type": insert_stmt.excluded.device_type,
                        "login_type": insert_stmt.excluded.login_type,
                    },
                )
                try:
                    # session.execute(upsert_stmt)
                    # session.commit()
                    if index == len(customer_df):
                        print("CUSTOMERS table populated succesfully")
                except Exception as e:
                    session.rollback()
                    print(f"Error: {e}")
        except Exception as e:
            print("Error populating 'CUSTOMERS' table")

        # #Orders
        try:
            orders_df = ecommerce_cleaned[
                ["customer_id", "order_date", "order_priority", "payment_method"]
            ]

            for index, row in orders_df.iterrows():
                insert_order = insert(Orders).values(
                    customer_id=row["customer_id"],
                    order_date=row["order_date"],
                    order_priority=row["order_priority"],
                    payment_method=row["payment_method"],
                )
                try:
                    # session.execute(insert_order)
                    # session.commit()
                    if index == len(orders_df):
                        print("ORDERS table populated succesfully")
                except Exception as e:
                    session.rollback()
                    print(f"Error: {e}")
        except Exception as e:
            print("Error populating 'ORDERS' table")

        # #Products
        try:
            products_df = (
                ecommerce_cleaned[["product_category", "product_name"]]
                .drop_duplicates()
                .reset_index()
            )
            
            for index, row in products_df.iterrows():
                insert_product = insert(Products).values(
                    product_category=row["product_category"], product_name=row["product_name"]
                )
                try:
                    # session.execute(insert_product)
                    # session.commit()
                    if index == len(products_df):
                        print("PRODUCTS table populated succesfully")
                except Exception as e:
                    session.rollback()
                    print(f"Error: {e}")
        except Exception as e:
            print("Error populating 'PRODUCTS' table")


        # #Order_Items
        try:

            def uuid_as_string(input_string):
                import re

                pattern = "'(.*?)'"
                matches = re.findall(pattern, input_string)
                return matches[0]

            from sqlalchemy import select, and_  # type: ignore
            import uuid

            order_ids = session.execute(select(Orders.order_uid)).fetchall()

            order_items_df = ecommerce_cleaned[
                [
                    "quantity",
                    "discount",
                    "profit",
                    "product_category",
                    "product_name",
                    "sales",
                    "shipping_cost",
                    "aging",
                ]
            ]

            for index, row in order_items_df.iterrows():
                cast_order_id = uuid.UUID(uuid_as_string(str(order_ids[index])))

                product_row = (
                    session.query(Products)
                    .filter(
                        and_(
                            Products.product_name == str(row["product_name"]),
                            Products.product_category == str(row["product_category"]),
                        )
                    )
                    .all()
                )

                for product_details in product_row:
                    product_id_from_products_table = product_details.product_uid

                insert_order_item = insert(Order_Items).values(
                    order_id=cast_order_id,
                    product_id=product_id_from_products_table,
                    quantity=int(row["quantity"]),
                    discount=float(row["discount"]),
                    profit=float(row["profit"]),
                    sales=float(row["sales"]),
                    shipping_cost=float(row["shipping_cost"]),
                    aging=float(row["aging"]),
                )
                try:
                    # session.execute(insert_order_item)
                    # session.commit()
                    if index == len(order_items_df):
                        print("ORDER_ITEMS table populated succesfully")
                except Exception as e:
                    session.rollback()
                    print(f"Error: {e}")

        except Exception as e:
            print("Error populating 'ORDER_ITEMS' table")

        print(f"{db_to_connect} database populated succesfully")
    else:
        print(f"{db_to_connect} database NOT populated")

if __name__ == "__main__":
    load_data_into_postgres(val=True)