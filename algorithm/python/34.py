while True:
    try:
        cuts = int(input())
    except:
        break
    pieces = int((cuts**3 + 5*cuts + 6) / 6)
    print(pieces)