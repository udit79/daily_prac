def remove_duplicates(ids: list[int]) -> int:
    if len(ids)==0:
        return 0
    ptr1=0
    ptr2=1
    for id in range(len(ids)-1):
        if ids[ptr1]!=ids[ptr2]:
            ptr1=ptr1+1
            ids[ptr1],ids[ptr2]=ids[ptr2],ids[ptr1]
        ptr2+=1
    ids[:]=ids[:ptr1+1]
    return len(ids)
cases = [
    [],
    [1],
    [1, 1, 1],
    [1, 2, 3],
    [1, 1, 2, 2, 2, 3, 4, 4],
    [5, 5, 7, 7, 9],
    [1, 1, 1, 2, 2, 3, 3, 3, 4],
]
count=1
for case in cases:
    print(f"Case No.{count}:")
    print("ids before function:",case)
    print("Length of id after function:",remove_duplicates(case))
    print("ids after function:",case)
    count+=1
