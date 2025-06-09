t = int(input())




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
            max_.insert(-1, other)
            max_.sort()
            max_.reverse()
            max_.pop()
            min_list = max_[-1]
    print(max_, sum_)
    sum_ += sum(max_)
    print(sum_)

        

