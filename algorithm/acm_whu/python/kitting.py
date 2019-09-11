class Point():
    def __init__(self,x,y):
        self.x = x
        self.y = y
    def equal(self,point):
        if point.x == self.x and point.y == self.y:
            return True
        else:
            return False
    def up(self):
        return (Point(self.x, self.y + 1))
    def down(self):
        return (Point(self.x, self.y - 1))
    def left(self):
        return (Point(self.x - 1, self.y))
    def right(self):
        return (Point(self.x + 1, self.y))
    def minDis(self,point):
        return int(abs(point.x - self.x) + abs(point.y - self.y))
    

def findPath(point,step):
    global count
    if step >= n:
        if point.equal(end):
            count = count + 1
        return
    elif point.minDis(end) > n - step:
        return
    else:
        findPath(point.up(),step + 1)
        findPath(point.down(),step + 1)
        findPath(point.left(),step + 1)
        findPath(point.right(),step + 1)

case_amount = int(input())
for index in range(case_amount):
    x1,y1,x2,y2,n = [int(i) for i in input().split()]
    start = Point(x1,y1)
    end = Point(x2,y2)
    count = 0
    findPath(start, 0)
    print(count)

    