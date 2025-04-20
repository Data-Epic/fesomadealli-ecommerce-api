
import uvicorn      #type: ignore
from fastapi import Depends, FastAPI        # type: ignore
from api import routes
from database.crud import Session

app = FastAPI(title="Ecommerce API")


def get_session():
    db = Session()
    try:
        yield db
    finally:
      db.close()      


@app.get("/customers/")
def get_all_customers(db: Session = Depends(get_session)):      # type: ignore
 resp = routes.get_customers(db, id="all")
 return resp


@app.get("/customers/{customer_id}")  #78489 81129 60783 63932 95513
def that_one_customer(id, db: Session = Depends(get_session)):        # type: ignore
 resp = routes.get_customers(db, id=id)
 return resp


@app.get("/orders/")
def get_all_orders(db: Session = Depends(get_session)):     # type: ignore
 resp = routes.get_orders(db, id="all")
 return resp


@app.get("/orders/{order_id}")  #65717dba-7341-422e-9c84-ca5901bab19f   'order_id': UUID('9ac712a6-894d-4773-985c-f76c4d3c5843')
def that_one_order(id, db: Session = Depends(get_session)):     # type: ignore
 resp = routes.get_orders(db, id=id)
 return resp


@app.get("/products/")
def get_all_products(db: Session = Depends(get_session)):       # type: ignore
 resp = routes.get_products(db, id="all")
 return resp


@app.get("/analytics/top-products/")
def top_products(db: Session = Depends(get_session)):       # type: ignore
 resp = routes.get_top_products(db)
 return resp


@app.get("/analytics/revenue/")
def revenue_profit(db: Session = Depends(get_session)):     # type: ignore
 resp = routes.revenue_and_profit(db)
 return resp 