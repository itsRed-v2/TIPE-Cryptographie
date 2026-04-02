import 

for k in range(6):
    num = numbers[k]
    print(num)

    start = time.time()
    total = num * num
    finish = time.time()
    elapsed = finish - start

    print(k, elapsed)