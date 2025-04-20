

import sys
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))


from database.crud import session
from database.models import Customers, Orders, Products, Order_Items
from scripts import insights

from sqlalchemy import func, desc   # type: ignore
import uuid
from uuid import UUID

query_error: dict = {"Message": "An Error Occured"}

query_resp = {}

def get_customers(db, id="all"):  
    query_resp: dict ={}
    if id != "all":
        try:
            resp: list = db.query(Customers).filter(Customers.customer_id == str(id)).all()
        except Exception as e:
            return query_error
    else:
        try:
            resp = db.query(Customers).all()
        except Exception as e:
            return query_error 

    for index, customer_obj in enumerate(resp):
        customer_info : dict = {
                        "customer_id" : customer_obj.customer_id,
                        "gender": customer_obj.gender,
                        "login_type": customer_obj.login_type,
                        "device_type": customer_obj.device_type
        }
        query_resp[index] = customer_info

    print(query_resp)
    return query_resp


def get_orders(db, id="all"):
    query_resp: dict = {}

    if id != "all":
        try:
            resp: list = db.query(Orders).filter(Orders.order_uid == uuid.UUID(id)).all()
        except Exception as e:
            return e #query_error
    else:
        try:
            resp: list = db.query(Orders).all()
        except Exception as e:
            return e #query_error
        
    print(f"Query returned {len(resp)} records.")
    for index, order_obj in enumerate(resp):
        order_info : dict = {
                        "order_id": order_obj.order_uid,
                        "order_date": order_obj.order_date,
                        "customer_id" : order_obj.customer_id,
                        "order_priority": order_obj.order_priority,
                        "payment_method": order_obj.payment_method
        }
        
        query_resp[index] = order_info
    
    print(query_resp)
    return query_resp


def get_products(db, id="all"):
    query_resp: dict = {}

    if id == "all":
        try:
            resp: list = db.query(Products).all()
        except Exception as e:
            return query_error
        
    for index, product_obj in enumerate(resp):
        query_resp[index] = product_obj
    
    print(query_resp)
    return query_resp


def get_top_products(db):
    query_resp: dict = {}

    try: 
        top_five_products = db.query(
            Products.product_name,
            func.sum(Order_Items.sales).label('total_sales')
            ).join(Products, Order_Items.product_id == Products.product_uid
            ).group_by(Products.product_name
            ).order_by(desc('total_sales')
            ).limit(5).all()
        
        for product, sales in top_five_products:
            query_resp[product] = sales
        
        print(query_resp)
        return query_resp
    
    except Exception as e:
        return query_error


def revenue_and_profit(db):
    query_resp: dict = {}
    try:
        total_revenue = db.query(func.sum(Order_Items.sales)).scalar()
        query_resp["Total Revenue"] = total_revenue
        total_profit = db.query(func.sum(Order_Items.profit)).scalar()
        query_resp["Total Profit"] = total_profit
        
        print(query_resp)
        return query_resp
    
    except Exception as e:
        return query_error
    
def db_insights(db):
    insights_dict = {}

    insights_dict["customer_resp"] = insights.customer_insights()
    insights_dict["product_resp"] = insights.product_insights()
    insights_dict["order_resp"] = insights.order_insights()
    
    print(insights_dict)
    return insights_dict


if __name__ == "__main__":
    get_customers(session)
    get_orders(session)
    get_products(session)
    get_top_products(session)
    revenue_and_profit(session)
    db_insights(session)