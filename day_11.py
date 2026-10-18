from collections.abc import Callable
from typing import TypeVar,Annotated
from pydantic import validate_call,Field
import random
import time
T=TypeVar("T")
@validate_call
def run_with_retry(
        operations:Callable[[],T],
        *,max_attempts:Annotated[int,Field(gt=0,strict=True,allow_inf_nan=False)]=3,
        base_delay:Annotated[float,Field(ge=0,allow_inf_nan=False)]=0.25,
        max_delay:Annotated[float,Field(strict=True,allow_inf_nan=False,ge=0)]=2.0,
        sleep_fn:Callable[[float],None]|None=None,
        random_fn:Callable[[],float]|None=None)->T: # type: ignore 
    for index in range(max_attempts):
        try:
            something=operations()
            return something
        except Exception as e:
            if index+1<max_attempts and  isinstance(e,(TimeoutError,ConnectionError)):
                if random_fn==None:
                    random_res=random.random()
                else:
                    random_res=random_fn()
                cap=min(max_delay,base_delay*(2**index))
                delay=random_res*cap
                if sleep_fn==None:
                    time.sleep(delay)
                else:
                    sleep_fn(delay)
                continue
            else:
                raise e
