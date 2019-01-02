import random

def holdAnimal():
    #config parameters
    total_animal_max = 100
    single_space_max = int(1e4)
    single_point_max = int(1e4)
    for i in range(case_num):
        a = int(random.random() * total_animal_max)
        print(a)
        count = 0
        for i in range(a):
            f = int(random.random() * single_space_max)
            s = int(random.random() * single_point_max)
            print("{f} {s}".format(f=f,s=s))
            count = count + f

        ts = int(count / 2)
        if ts > 1e5:
            ts = int(1e5)

        print(ts)

def cherryblossom():
    symmetry = False
    total_point_max = 100
    coor_max = 10000
    for i in range(case_num):
        s = []
        point_amount = int(random.random() * total_point_max / 2) * 2
        print(point_amount)
        axis = int(random.random() * coor_max)
        for j in range(point_amount):
            if len(s) != 0:
                x, y = s.pop()
                print("{x} {y}".format(x=x,y=y))
                continue
            x = int(random.random()*coor_max)
            y1 = int(random.random() * axis)
            if symmetry is True:
                y2 = 2 * axis - y1
                s.append((x,y2))
            print("{x} {y}".format(x=x,y=y1))
        
def thinkandcount():
    MAX = 2000
    for i in range(case_num):
        row = int(random.random() * MAX)
        col = int(random.random() * MAX)
        
        def rand_letter():
            num = int(random.random() * 2) 
            if num is 0:
                return 'w'
            else:
                return 'b'
        print("{row} {col}".format(row=row,col=col))
        for i in range(row):
            row_content = [rand_letter() for i in range(col)]
            print(''.join(row_content))



case_num = 3
generator = cherryblossom

generator()