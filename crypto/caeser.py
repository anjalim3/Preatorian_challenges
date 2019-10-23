string = "JxqebjxqfzxiLypbosbaObcibzqflk"
sol = ""
for letter in string:
    sol = sol+ str(chr((ord(letter) + 3)))

print sol