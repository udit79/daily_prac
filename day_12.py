from collections import OrderedDict
from pydantic import validate_call,Field,StrictInt
from typing import Annotated
class LRUCache:
    @validate_call
    def __init__(self, capacity: Annotated[StrictInt,Field(gt=0)]):
        self.cache=OrderedDict()
        self.capacity=capacity
    def get(self, key: str) -> str | None:
        value=self.cache.get(key)
        if value is not None:
            self.cache.move_to_end(key)
        return value
    def put(self, key: str, value: str) -> None:
        if key in self.cache:
            self.cache.move_to_end(key)
        self.cache[key]=value
        if len(self.cache)>self.capacity:
            self.cache.popitem(last=False)
        return 
if __name__ == "__main__":
    store=LRUCache(capacity=2)
    store.put("A", "alpha")
    store.put("B", "beta")
    res=store.get("A")
    print(res)
    store.put("C", "gamma")
    res=store.get("B")
    print(res)
    res=store.get("A")
    print(res)
        
