import random
from sympy import isprime, nextprime, primitive_root, gcd

def encrypt(message, p, g, b):
    encrypted_blocks = []
    for block in message:
        while True:
            k = random.randint(1, p-1)  # Генеруємо випадкове число k
            if gcd(k, p-1) == 1:  # Перевіряємо, чи є k і (p-1) взаємно простими
                break

        r = pow(g, k, p)
        m = int.from_bytes(block.encode(), 'big')
        y = (pow(b, k, p) * m) % p

        encrypted_blocks.append((r, y))

    return encrypted_blocks

def decrypt(encrypted_blocks, p, a):
    decrypted_message = ""
    for block in encrypted_blocks:
        r, y = block
        s = pow(r, a, p)
        m = (y * pow(s, -1, p)) % p
        decrypted_block = hex(m)[2:]  # Перетворюємо числове значення у шістнадцятковий рядок
        decrypted_message += bytearray.fromhex(decrypted_block).decode()  # Перетворюємо шістнадцятковий рядок у текст

    return decrypted_message


# Згенерувати випадкове просте число p і його первісний корінь g
bit_length = random.randint(20, 40)  # Випадкова довжина біта

while True:
    p = nextprime(random.getrandbits(bit_length))
    if isprime(p):
        break

g = primitive_root(p)

# Згенеруйте випадковий закритий ключ a та обчисліть відкритий ключ b
a = random.randint(1, p-1)
b = pow(g, a, p)

# Отримати вхідне повідомлення від користувача
message = input("Введіть повідомлення: ")

# Розділити повідомлення на блоки заданого розміру (наприклад, 8 символів)
block_size = 8
message_blocks = [message[i:i+block_size] for i in range(0, len(message), block_size)]

# Зашифруйте повідомлення
encrypted_blocks = encrypt(message_blocks, p, g, b)
print("Зашифровані блоки:", encrypted_blocks)

# Розшифруйте повідомлення
decrypted_message = decrypt(encrypted_blocks, p, a)
print("Розшифроване повідомлення:", decrypted_message)
