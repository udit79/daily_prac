orders = [
    {"order_id": "A101", "status": "pending",   "updated_at": 10},
    {"order_id": "B205", "status": "shipped",   "updated_at": 12},
    {"order_id": "A101", "status": "delivered", "updated_at": 18},
    {"order_id": "A101", "status": "shipped",   "updated_at": 15},
    {"order_id": "C301", "status": "pending",   "updated_at": 11},
    {"order_id": "B205", "status": "delivered", "updated_at": 20},
]
orders_3 = [
    {"order_id": "A101", "status": "delivered", "updated_at": 30},
    {"order_id": "A101", "status": "pending", "updated_at": 10},
    {"order_id": "A101", "status": "shipped", "updated_at": 20},
]
orders_4 = [
    {"order_id": "A101", "status": "pending", "updated_at": 10},
    {"order_id": "A101", "status": "shipped", "updated_at": 10},
    {"order_id": "A101", "status": "delivered", "updated_at": 10},
]
orders_5 = [
    {"order_id": "A101", "status": "pending", "updated_at": 5},
    {"order_id": "B202", "status": "shipped", "updated_at": 8},
    {"order_id": "C303", "status": "cancelled", "updated_at": 3},
]
orders_6 = [
    {"order_id": "X1", "status": "created", "updated_at": 1},
    {"order_id": "X1", "status": "paid", "updated_at": 5},
    {"order_id": "X1", "status": "processing", "updated_at": 3},
    {"order_id": "X1", "status": "shipped", "updated_at": 8},
    {"order_id": "X1", "status": "delivered", "updated_at": 7},
]
def get_latest_order_status(orders: list[dict]) -> dict[str, str]:
    latest_state={}
    for order in orders:
        order_id=order["order_id"]
        if order_id not in latest_state or int(latest_state[order_id].split("-")[1])<=order["updated_at"]:
            latest_state[order_id]=f"{order["status"]}-{str(order["updated_at"])}"
    for order_id,status_str in latest_state.items():
        latest_state[order_id]=status_str.split("-")[0]
    return latest_state
print(f"case1:\n\tDataset:\n\t\t{orders}\n\tResult:\n\t\t{get_latest_order_status(orders)}")
print(f"case2:\n\tDataset:\n\t\t{[]}\n\tResult:\n\t\t{get_latest_order_status([])}")
print(f"case3:\n\tDataset:\n\t\t{orders_3}\n\tResult:\n\t\t{get_latest_order_status(orders_3)}")
print(f"case4:\n\tDataset:\n\t\t{orders_4}\n\tResult:\n\t\t{get_latest_order_status(orders_4)}")
print(f"case5:\n\tDataset:\n\t\t{orders_5}\n\tResult:\n\t\t{get_latest_order_status(orders_5)}")
print(f"case6:\n\tDataset:\n\t\t{orders_6}\n\tResult:\n\t\t{get_latest_order_status(orders_6)}")