products = [
    {"id": 101, "name": "Wireless Mouse", "price": 799, "rating": 4.3, "category": "electronics"},
    {"id": 102, "name": "Mechanical Keyboard", "price": 3499, "rating": 4.7, "category": "electronics"},
    {"id": 103, "name": "Laptop Stand", "price": 999, "rating": 4.4, "category": "accessories"},
    {"id": 104, "name": "USB-C Hub", "price": 1299, "rating": 4.2, "category": "electronics"},
    {"id": 105, "name": "Desk Lamp", "price": 1599, "rating": 4.6, "category": "home"},
    {"id": 106, "name": "Monitor Arm", "price": 2499, "rating": 4.5, "category": "accessories"},
    {"id": 107, "name": "Webcam", "price": 1999, "rating": 4.1, "category": "electronics"},
    {"id": 108, "name": "Office Chair", "price": 8999, "rating": 4.8, "category": "furniture"},
]
def filter_products(products, min_price=None, max_price=None, min_rating=None, category:str|None=None)->list:
    filtered_list=[]
    for product in products:
        price=product["price"]
        rating=product.get("rating",None)
        cat=product["category"].lower()
        if max_price==None:
            max_price=float('inf')
        if min_price==None:
            min_price=float('-inf')
        if min_rating==None:
            min_rating=0
        if (min_price<=price<=max_price) and min_rating<=rating and (category is None or category.lower()==cat ):
            filtered_list.append(product["id"])
    return filtered_list
print("Case 1:",filter_products(products, min_price=1000, max_price=3000))
print("Case 2:",filter_products(products, min_rating=4.5))
print("Case 3:",filter_products(products, category="ELECTRONICS"))
print("Case 4:",filter_products(
    products,
    min_price=1000,
    max_price=3000,
    min_rating=4.5,
    category="electronics"
))
print("Case 5:",filter_products(products))
print("Case 6:",filter_products(products, min_price=10000))