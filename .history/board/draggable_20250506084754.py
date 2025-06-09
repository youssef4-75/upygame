t = int(input())

def exch[A](l: list[A], x: A):
    for i, a in enumerate(l):
        if x>=a:
            break
    l.insert(i, x)
    l.pop()


for _ in range(t):
    n, k = [int(i) for i in input().split()]
    left = [int(i) for i in input().split()]
    right = [int(i) for i in input().split()]
    max_ = [0 for _ in range(k-1)]
    min_list = 0
    sum_ = 0
    for i in range(n): 
        if left[i] > right[i]:
            right[i], left[i] = left[i],

    sum_ += sum(max_) + 1
    print(sum_)

        

