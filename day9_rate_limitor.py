def max_window_sum(numbers: list[int], window_size: int) -> int:
    if len(numbers)<window_size:
        return 0 
    if window_size<=0:
        return 0
    start=0
    end=start+window_size-1
    max_sum=float("-inf")
    window_sum=0
    for index,num in enumerate(numbers):
        if index<end:
            window_sum+=num
        elif index==end:
            window_sum+=num
            max_sum=max(max_sum,window_sum)
        elif index>end:
            window_sum-=numbers[start]
            start+=1
            end+=1
            window_sum+=num
    if max_sum==float("-inf"):
        return 0
        
    return int(max_sum)
cases = [
    ([2, 1, 5, 1, 3, 2], 3),
    ([5], 1),
    ([1, 2, 3], 2),
    ([-5, -2, -8], 2),
    ([1, 2], 3),
    ([], 3),
    ([1, 2, 3], 0),
]
count=1
for case in cases:
    print(f"Case No.{count}:")
    print("case:",case)
    print("max_sum:",max_window_sum(case[0],case[1]))
    count+=1
