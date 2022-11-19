k = int(input())
l = int(input())
m = int(input())
n = int(input())
d = int(input())
drags = []
count = 0
for i in range(d):
    if (i+1) % k == 0:
        count += 1
    else:
        if (i+1) % l == 0:
            count += 1
        else:
            if (i+1) % m == 0:
                count += 1
            else:
                if (i+1) % n == 0:
                    count += 1
print(count)
