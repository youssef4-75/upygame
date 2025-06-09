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
    for i in range(n): 
        if left[i] > right[i]:
            right[i], left[i] = left[i], right[i]
    
    left.sort(reverse=True)
    sum_ = sum(right) + sum(left[:k-1]) + 1
    print(sum_)

        

