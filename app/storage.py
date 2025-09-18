
from dataclasses import dataclass
@dataclass
class OrderDraft:
    material: str|None=None
    quantity_value: str|None=None
    quantity_unit: str|None=None  # "pcs" | "m2"
    delivery_type: str|None=None  # "warehouse" | "site"
    delivery_address: str|None=None
    name: str|None=None
    phone: str|None=None
    email: str|None=None
