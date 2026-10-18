products = [
    {"id": 101, "name": "Wireless Mouse", "price": 799, "rating": 4.3},
    {"id": 102, "name": "Mechanical Keyboard", "price": 3499, "rating": 4.7},
    {"id": 103, "name": "Wireless Headphones", "price": 2499, "rating": 4.5},
    {"id": 104, "name": "USB-C Hub", "price": 1299, "rating": 4.2},
    {"id": 105, "name": "Gaming Mouse", "price": 1499, "rating": 4.6},
    {"id": 106, "name": "Wireless Keyboard", "price": 2999, "rating": 4.7},
    {"id": 107, "name": "Laptop Stand", "price": 999, "rating": 4.4},
    {"id": 108, "name": "Gaming Headset", "price": 1999, "rating": 4.6},
]
def search_products(products:list[dict],query:str,limit:int)->list[dict]:
    if products ==[]:
        return []
    if query is None or not query.strip():
        return []
    if limit<=0:
        return []
    filtered_results=[]
    query=query.lower()
    for product in products:
        if query in product["name"].lower() :
            filtered_results.append(product)
    if len(filtered_results)==0 :
        return []
    filtered_results=sorted(filtered_results,key=lambda x:(-x["rating"],x["price"]))
    return filtered_results[:limit]
print(search_products(products, "mouse", 0))