x = int(input("quanti numero vuoi inserire?\n> "))
max = int(input("inserisci il primo numero:\n> "))

for i in range(x - 1):
    z = input("inserisci un numero:\n> ")
    z = int(z)
    if z > max:
        max = z

print(max)
