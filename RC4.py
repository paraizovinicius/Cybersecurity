def encrypt(key, plaintext):
    S = list(range(256))
    j = 0
    out = []

    # Converte a chave em uma lista de inteiros
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
        out.append(chr(ord(char) ^ S[(S[i] + S[j]) % 256]))

    return ''.join([str(c) for c in out])


def decrypt(key, ciphertext):
    S = list(range(256))
    j = 0
    out = []

    # Converte a chave em uma lista de inteiros
    key = [ord(c) for c in key]

    # Key-Scheduling Algorithm (KSA)
    for i in range(256):
        j = (j + S[i] + key[i % len(key)]) % 256
        S[i], S[j] = S[j], S[i]

    # Pseudo-Random Generation Algorithm (PRGA)
    i = j = 0
    for char in ciphertext:
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]
        out.append(chr(ord(char) ^ S[(S[i] + S[j]) % 256]))

    return ''.join(str(c) for c in out)

# used as an entrance to KSA, witch generates an initial permutation of array S
key = '20202021'
iv = "123456"  # Grants that the same key won't generate the same stream of cryptographed bits every time is used
plaintext = 'Hello, world!'

ciphertext = encrypt(key, plaintext)
print('Cipher text:', ciphertext)

decrypted = decrypt(key, ciphertext)
print('Recovered plaintext: ', decrypted)
