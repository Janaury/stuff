case_amount = int(input())

for index in range(case_amount):
    n = int(input())
    if (n + 14)%14 == 0:
        print("snoopy wins the game!")
    else:
        print("flymouse wins the game!");