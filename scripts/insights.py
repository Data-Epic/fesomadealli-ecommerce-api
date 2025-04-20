
import sys
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from database.db_setup import engine
from database.models import Customers, Orders, Products, Order_Items
from database.crud import session

from sqlalchemy import func, desc # type: ignore


# Customer Insights
def customer_insights():
    customer_insights: dict = {}

    unique_customers = session.query(func.count(Customers.customer_id.distinct())).scalar()
    customer_insights["Total Number of Unique Customers"] = unique_customers

    # Number of customers per device type (Web/Mobile)
    customer_per_device = session.query(Customers.device_type, 
                                        func.count(Customers.customer_id)
                                        ).group_by(Customers.device_type).all()
    
    for device_users_tuple in customer_per_device:
        device, users = device_users_tuple
        customer_insights[f"Number of {device} Users"] = str(users)

    # Percentage of Members vs. Guest users.
    members_vs_guests = session.query(Customers.login_type, 
                                        func.count(Customers.customer_id)
                                        ).group_by(Customers.login_type).all()
    
    for _tuple in members_vs_guests:
        login_type, num_of_users = _tuple
        customer_insights[f"Percentage of {login_type} Users"] = f"{round(((num_of_users/unique_customers) *100),2)}%"
    
    return customer_insights


inner_join_query = session.query(Order_Items, Products).join(Products, 
                                                                Order_Items.product_id == Products.product_uid
                                                                ).limit(5).all()


# Product Performance Insights
def product_insights():
    product_insights: dict = {}

    top_five_products = session.query(
            Products.product_name,
            func.sum(Order_Items.sales).label('total_sales')
            ).join(Products, Order_Items.product_id == Products.product_uid
            ).group_by(Products.product_name
            ).order_by(desc('total_sales')
            ).limit(5).all()

    for product, sales in top_five_products:
        product_insights[product] = sales

    top_three_categories = session.query(
            Products.product_category,
            func.sum(Order_Items.profit).label('total_profit')
            ).join(Products, Order_Items.product_id == Products.product_uid
            ).group_by(Products.product_category
            ).order_by(desc('total_profit')
            ).limit(3).all()

    for category, profit_made in top_three_categories:
        product_insights[f"({category})"] = f"Profit: {profit_made}"
    
    return product_insights


# Order Analysis
def order_insights():
    order_insights: dict = {}

    # Average Order size (quantity per order).
    total_qty_ordered = session.query(func.sum(Order_Items.quantity)).scalar()
    total_num_of_orders = session.query(Orders.order_uid).count()
    order_insights["Avg Order Size"] = f"{total_qty_ordered/total_num_of_orders}"


    # Total revenue and profit
    total_revenue = session.query(func.sum(Order_Items.sales)).scalar()
    total_profit = session.query(func.sum(Order_Items.profit)).scalar()
    order_insights[f"Total Profit | Total Revenue"] = f"{total_profit} | {total_revenue}"
          
    # Percentage of orders placed with High or Critical priority.
    priority_of_orders = session.query(Orders.order_priority, 
                                        func.count(Orders.customer_id)
                                        ).group_by(Orders.order_priority).all()
    for _tuple in priority_of_orders:
        priority_type, num_of_orders = _tuple
        order_insights[f"Percentage of {priority_type} Users"] = f"{round(((num_of_orders/total_num_of_orders) *100),2)}%"

    # Discount Impact
    sales_vs_discount = session.query(
                        Order_Items.discount, 
                        func.sum(Order_Items.sales)
                        ).group_by(Order_Items.discount).all()
    dis_sale_dict ={}
    for discount, sale in sales_vs_discount:
        dis_sale_dict[discount] = sale

    dis_sale_sorted = {key: val for key, val in sorted(dis_sale_dict.items(), 
                                                    key = lambda sort_by_values: sort_by_values[1])}    

    order_insights["Discount_And_Sales"] = dis_sale_sorted

    return order_insights

if __name__ == "__main__":
    customer_insights()
    product_insights()
    order_insights()