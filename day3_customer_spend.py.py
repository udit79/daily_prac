orders = orders_no_completed = orders_single_customer = []
def summarize_customer_spend(orders:list[dict])->dict:
    summarize_report={}
    for order in orders:
        if order["status"]=="completed":
            summarize_report[order["customer_id"]]=summarize_report.get(order["customer_id"],0)+order["amount"]
    return summarize_report
print(f"case1:\n\tDataset:\n\t\t{orders}\n\tResult:\n\t\t{summarize_customer_spend(orders)}")