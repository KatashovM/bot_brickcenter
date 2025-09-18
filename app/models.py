
from sqlalchemy import create_engine, Integer, String, Text, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker
from datetime import datetime
class Base(DeclarativeBase): pass
class Order(Base):
    __tablename__ = "orders"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    material: Mapped[str] = mapped_column(String(255))
    quantity_value: Mapped[str] = mapped_column(String(64))
    quantity_unit: Mapped[str] = mapped_column(String(16))  # pcs | m2
    delivery_type: Mapped[str] = mapped_column(String(32))  # warehouse | site
    delivery_address: Mapped[str] = mapped_column(Text, default="")
    name: Mapped[str] = mapped_column(String(255))
    phone: Mapped[str] = mapped_column(String(64))
    email: Mapped[str] = mapped_column(String(255))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
def make_engine(db_path: str):
    return create_engine(f"sqlite+pysqlite:///{db_path}", echo=False)
def init_db(engine): Base.metadata.create_all(engine)
Engine = None; SessionLocal = None
def setup_db(db_path: str):
    global Engine, SessionLocal
    Engine = make_engine(db_path); init_db(Engine); SessionLocal = sessionmaker(bind=Engine)
