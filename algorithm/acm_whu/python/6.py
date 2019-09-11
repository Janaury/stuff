# 广度优先搜索
cp= dict() #communication_graph 
animal_amount, pair_amount = [int(i) for i in input().split()]


def findMin(one, other):
    queue = []
    visited = dict()
    queue.append(one)
    visited[one] = one
    count = -1
    while len(queue) != 0:
        now = queue.pop(0)
        if now != other:
            try:
                for item in cp[now]:
                    if item not in visited.keys():
                        queue.append(item)
                        visited[item] = now
            except:
                break
        else:
            count = 0
            while(visited[now] != one):
                count = count + 1
                now = visited[now]
                break
    print(count)

                
for i in range(pair_amount):
    one, other = [int(j) for j in input().split()]
    if one not in cp.keys():
        cp[one] = []
    if other not in cp.keys():
        cp[other] = []

    cp[one].append(other)
    cp[other].append(one)

query_amount = int(input())
for i in range(query_amount):
    one, other = [int(i) for i in input().split()]
    findMin(one, other)
