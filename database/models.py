import uuid
from sqlalchemy.ext.declarative import declarative_base  # type: ignore
from sqlalchemy import ForeignKey, Column, String, Integer, Numeric, UUID, Date  # type: ignore
from sqlalchemy.dialects.postgresql import UUID  # type: ignore


Base = declarative_base()


class Customers(Base):
    __tablename__ = "customers"
    customer_uid = Column(
        "id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    customer_id = Column("customer_id", String, unique=True, nullable=False)
    gender = Column("gender", String, nullable=False)
    device_type = Column("device_type", String)
    login_type = Column("login_type", String)

    def __repr__(self):
        return f"<Customer(customer_id={self.customer_id}, gender={self.gender}, device_type={self.device_type}, login_type={self.login_type})>\n"


class Orders(Base):
    __tablename__ = "orders"
    order_uid = Column("id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    customer_id = Column("customer_id", String, ForeignKey("customers.customer_id"))
    order_date = Column("order_date", Date)
    order_priority = Column("order_priority", String)
    payment_method = Column("payment_method", String)

    def __repr__(self):
        return f"<Order(order_id={self.order_uid}, customer_id={self.customer_id}, order_date={self.order_date}, order_priority={self.order_priority}, payment_method={self.payment_method})>\n"


class Products(Base):
    __tablename__ = "products"
    product_uid = Column("id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    product_category = Column("product_category", String)
    product_name = Column("product_name", String)

    def __repr__(self):
        return f"<Product(product_id={self.product_uid}, product_category={self.product_category}, product_name={self.product_name})>\n"


class Order_Items(Base):
    __tablename__ = "order_items"
    order_items_uid = Column(
        "id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    order_id = Column(
        "order_id", UUID(as_uuid=True), ForeignKey("orders.id"), nullable=False
    )
    product_id = Column(
        "product_id", UUID(as_uuid=True), ForeignKey("products.id"), nullable=False
    )
    quantity = Column("quantity", Integer)
    discount = Column("discount", Numeric(5, 2))
    sales = Column("sales", Numeric(10, 2))
    profit = Column("profit", Numeric(10, 2))
    shipping_cost = Column("shipping_cost", Numeric(10, 2))
    aging = Column("aging", Numeric(10, 2))

    def __repr__(self):
        return f"<Order Item(item_id={self.order_items_uid}, quantity={self.quantity}, discount={self.discount}, sales={self.sales}, profit={self.profit}, shipping_cost={self.shipping_cost}, delivery_time(in hours)={self.aging})>\n"

