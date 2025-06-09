t = int(input())

def insert_dicho[A](list_: list[A], elmt: A):
    start = 0
    end = len(list_)
    while end > start:
        mid = (end-start)//2 
        if list_[mid] > elmt:
            end = mid 
        elif list_[mid] < elmt: 
            start = mid 
        else: 
            list_.insert(mid, elmt)
            return mid
    list_.insert(start, elmt)
    return start 


for _ in range(t):
    n, k = [int(i) for i in input().split()]
    left = [int(i) for i in input().split()]
    right = [int(i) for i in input().split()]
    max_ = [0 for _ in range(k-1)]
    min_list = 0
    sum_ = 0
    for i in range(n): 
        sum_ += max(left[i], right[i])
        other = min(left[i], right[i])
        if other > min_list:
            insert_dicho(max_, other)
            max_.pop()
            min_list = max_[-1]
        

