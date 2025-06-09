t = int(input())

def exch[A](l: list[A], x: A):
    for i, a in enumerate(l):
        if x>=a:
            break
        
    l.pop()


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
        if not max_: continue
        if other > min_list:
            exch(max_, other)
            min_list = max_[-1]
    sum_ += sum(max_) + 1
    print(sum_)

        

