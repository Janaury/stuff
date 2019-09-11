def index(a):
    start_code = ord('a')
    return ord(a) - start_code

while True:
    try:
        bracelet = input()
    except:
        break
    length = len(bracelet)
    strings = [i for i in range(length)]
    sort_list = [[] for i in range(26)]

    for i in range(length - 1, -1, -1):
        for j in range(length):
            ch_index = (strings[j] + i) % length
            sort_index = index(bracelet[ch_index])
            sort_list[sort_index].append(strings[j])
        count = 0
        for item in sort_list:
            while len(item) != 0:
                strings[count] = item.pop(0)
                count = count + 1
            if count is length:
                break

    print(bracelet[strings[0]:] + bracelet[0:strings[0]])
            
