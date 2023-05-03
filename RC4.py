def rc4(key, plaintext):
    S = list(range(256))
    j = 0
    saida = []
    
    # Converts the key to a list of integers
    key = [ord(c) for c in key]

    # Key-Scheduling Algorithm (KSA)
    for i in range(256):
        j = (j + S[i] + key[i % len(key)]) % 256
        S[i], S[j] = S[j], S[i]

    # Pseudo-Random Generation Algorithm (PRGA)
    i = j = 0
    for char in plaintext:
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]
        # chr() converts an int in its equivalent ASCII
        # ord() converts a character ASCII in its numeric equivalent
        saida.append(chr(ord(char) ^ S[(S[i] + S[j]) % 256])) 
        
    # join() concatenates the elements in a list in a single string
    # In here, the use of a void string as a separator determines that there won't be a any char added between the elements of the resulting string
    # In addition, join() expects a list of strings, but saida contains a list of characters, so `str(c) for c in saida` is needed
    return ''.join(str(c) for c in saida) 



key = '12345678' # used as an entrance to KSA, witch generates an initial permutation of array S
plaintext = 'Hello, world!'
print(plaintext)
ciphertext = rc4(key, plaintext)
print('Texto criptografado:', ciphertext)

