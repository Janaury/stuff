str_nums = input().split()
h = set()
nums = []
for item in str_nums:
    num = int(item)
    if num == 0:
        break
    if num not in h:
        h.add(num)
        nums.append(num)
nums.sort()
for i in range(len(nums)):
    print(nums[i], end='')
    if i != len(nums) - 1:
        print('', end=' ')
print()
