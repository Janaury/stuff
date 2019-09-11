while True:
    cipher = input()
    result = []
    if cipher == "$":
        break
    else:
        for i in range(len(cipher)):
            n = ord(cipher[i]) - ord('A') - i - 1
            while n < 0:
                n = n + 26
            result.append(chr(n + ord('A')))
        print(''.join(result))