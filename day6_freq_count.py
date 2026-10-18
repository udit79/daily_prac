requests = [
    {"endpoint": "/users", "status": 200},
    {"endpoint": "/orders", "status": 200},
    {"endpoint": "/users", "status": 500},
    {"endpoint": "/products", "status": 200},
    {"endpoint": "/orders", "status": 200},
    {"endpoint": "/users", "status": 200},
    {"endpoint": "/orders", "status": 500},
    {"endpoint": "/products", "status": 200},
]
def most_requested_endpoint(requests: list[dict]) -> str | None:
    freq={}
    for req in requests:
        endpoint=req["endpoint"]
        freq[endpoint]=freq.get(endpoint,0)+1
    try:
        max_key,_=min(freq.items(),key=lambda x:(-x[1],x[0]))
    except ValueError:
        max_key=None
    return max_key
print(f"case1:\n\tDataset:\n\t\t{requests}\n\tResult:\n\t\t{most_requested_endpoint(requests)}")
print(f"case2:\n\tDataset:\n\t\t{[]}\n\tResult:\n\t\t{most_requested_endpoint([])}")
