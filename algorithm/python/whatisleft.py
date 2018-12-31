while True:
    book_include = set()
    try:
        book_amount = int(input())
    except:
        break
    books = [int(i) for i in input().split()]
    for i in range(book_amount):
        if books[i] in book_include:
            books[i] = -1
        else:
            book_include.add(books[i])
    books.sort()
    for item in books:
        if item != -1:
            print(item, end=' ')
    print()
