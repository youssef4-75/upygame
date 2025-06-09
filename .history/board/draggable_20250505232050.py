t = int(input())

for _ in range(t):
    n, k = [int(i) for i in input().split()]
    left = [int(i) for i in input().split()]
    right = [int(i) for i in input().split()]
    max_ = [0 for _ in range(k-1)]
    sum_ = 0
    for i in range(n): 
        sum_ += max(left[k], right[k])
        other = min(left[i], )