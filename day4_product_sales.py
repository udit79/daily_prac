order_items = [
    {
        "order_id": 1001,
        "product_id": 101,
        "quantity": 2,
        "unit_price": 500,
        "status": "completed",
    },
    {
        "order_id": 1001,
        "product_id": 102,
        "quantity": 1,
        "unit_price": 1200,
        "status": "completed",
    },
    {
        "order_id": 1002,
        "product_id": 101,
        "quantity": 1,
        "unit_price": 500,
        "status": "completed",
    },
    {
        "order_id": 1003,
        "product_id": 103,
        "quantity": 3,
        "unit_price": 800,
        "status": "cancelled",
    },
    {
        "order_id": 1004,
        "product_id": 101,
        "quantity": 4,
        "unit_price": 450,
        "status": "completed",
    },
    {
        "order_id": 1005,
        "product_id": 102,
        "quantity": 2,
        "unit_price": 1200,
        "status": "completed",
    },
    {
        "order_id": 1006,
        "product_id": 103,
        "quantity": 2,
        "unit_price": 750,
        "status": "completed",
    },
    {
        "order_id": 1007,
        "product_id": 101,
        "quantity": 1,
        "unit_price": 450,
        "status": "refunded",
    },
]
cancelled_orders = [
    {
        "order_id": 2001,
        "product_id": 101,
        "quantity": 5,
        "unit_price": 500,
        "status": "cancelled",
    },
    {
        "order_id": 2002,
        "product_id": 102,
        "quantity": 2,
        "unit_price": 1000,
        "status": "refunded",
    },
]
single_product = [
    {
        "order_id": 3001,
        "product_id": 999,
        "quantity": 2,
        "unit_price": 100,
        "status": "completed",
    },
    {
        "order_id": 3002,
        "product_id": 999,
        "quantity": 3,
        "unit_price": 150,
        "status": "completed",
    },
]
def summarize_product_sales(order_items:list[dict])->dict:
    final_matrix={}
    for item in order_items:
        if item["status"]=="completed":
            if item["product_id"] not in final_matrix.keys():
                item_matrix={}
            else:
                item_matrix=final_matrix[item["product_id"]]
            item_matrix["total_quantity"]=item_matrix.get("total_quantity",0)+item["quantity"]
            item_matrix["total_revenue"]=item_matrix.get("total_revenue",0)+(int(item["quantity"])*item["unit_price"])
            item_matrix["order_count"]=item_matrix.get("order_count",0)+1
            final_matrix[item["product_id"]]=item_matrix
    return final_matrix
print(f"case1:\n\tDataset:\n\t\t{single_product}\n\tResult:\n\t\t{summarize_product_sales(single_product)}")