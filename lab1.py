import random


def s_des_encrypt(plain_text, key, type):
    # Перестановка
    init_permutation = [2, 6, 3, 1, 4, 8, 5, 7]
    permuted_text = [plain_text[i - 1] for i in init_permutation]

    # Разделение на 2 части
    l0 = permuted_text[:4]
    r0 = permuted_text[4:]

    # Генерация ключей (10 бит на 8 бит)
    key_permutation1 = [3, 5, 2, 7, 4, 10, 1, 9, 8, 6]
    key_permutation2 = [6, 3, 7, 4, 8, 5, 10, 9]

    k1 = [key[i - 1] for i in key_permutation1]
    #разделение ключа на левую и правую часть
    k_0 = k1[:5]
    k_1 = k1[5:]

    #сдвиг влево на 1 для каждой части (первый подключ)
    k_0 = k_0[1:] + k_0[:1]
    k_1 = k_1[1:] + k_1[:1]
    k1 = k_0 + k_1
    k1 = [k1[i - 1] for i in key_permutation2]

    #сдвиг влево на 2 для каждой части (второй подключ)
    k_0 = k_0[2:] + k_0[:2]
    k_1 = k_1[2:] + k_1[:2]
    k2 = k_0 + k_1
    k2 = [k2[i - 1] for i in key_permutation2]
    if type == False:
        k1, k2 = k2, k1
    # 1-ый раунд функции
    # Расширение
    exp_permutation = [4, 1, 2, 3, 2, 3, 4, 1]
    r0_expanded = [r0[i - 1] for i in exp_permutation]

    # XOR с ключом (Отбеливатель)
    r0_expanded_xor_key = [r0_expanded[i] ^ k1[i] for i in range(8)]

    # S-Box
    sbox_permutation = [
        [[1, 0, 3, 2], [3, 2, 1, 0], [0, 2, 1, 3], [3, 1, 3, 2]],
        [[0, 1, 2, 3], [2, 0, 1, 3], [3, 0, 1, 0], [2, 1, 0, 3]],
    ]

    lsb = r0_expanded_xor_key[:4]
    row = 2 * lsb[0] + lsb[3]
    col = 2 * lsb[1] + lsb[2]

    out = sbox_permutation[0][row][col]
    out_l = [out // 2, out % 2]
    msb = r0_expanded_xor_key[4:]
    row = 2 * msb[0] + msb[3]
    col = 2 * msb[1] + msb[2]

    out = sbox_permutation[1][row][col]
    out_l = out_l + [out // 2, out % 2]

    # прямая перестановка
    permutation = [2, 4, 3, 1]
    output = [out_l[i - 1] for i in permutation]

    # XOR с левой половиной
    r1 = [output[i] ^ l0[i] for i in range(4)]
    l1 = r0

    # 2-ой раунд функции
    # Расширение
    r1_expanded = [r1[i - 1] for i in exp_permutation]

    # XOR с ключом (Отбеливатель)
    r1_expanded_xor_key = [r1_expanded[i] ^ k2[i] for i in range(8)]

    # S-Box
    lsb = r1_expanded_xor_key[:4]
    row = 2 * lsb[0] + lsb[3]
    col = 2 * lsb[1] + lsb[2]
    out = sbox_permutation[0][row][col]
    out_l = [out // 2, out % 2]

    msb = r1_expanded_xor_key[4:]
    row = 2 * msb[0] + msb[3]
    col = 2 * msb[1] + msb[2]
    out = sbox_permutation[1][row][col]
    out_l = out_l + [out // 2, out % 2]

    # прямая перестановка
    output = [out_l[i - 1] for i in permutation]

    # XOR с левой половиной
    l2 = [output[i] ^ l1[i] for i in range(4)]
    r2 = r1
    out = l2 + r2

    # Конечная перестановка
    final_permutation = [4, 1, 3, 5, 7, 2, 8, 6]
    cipher_text = [out[i - 1] for i in final_permutation]
    return cipher_text


m = [int(bit) for bit in bin(random.randrange(255))[2:]]
m = [0 for i in range(0, 8 - len(m))] + m

k1 = [int(bit) for bit in bin(random.randrange(1024))[2:]]
k1 = [0 for i in range(0, 10 - len(k1))] + k1

k2 = [int(bit) for bit in bin(random.randrange(1024))[2:]]
k2 = [0 for i in range(0, 10 - len(k2))] + k2

h = s_des_encrypt(s_des_encrypt(m, k1, True), k2, True)

m_enc = {}
h_dec = {}
#зашифруем m - открытый текст всеми ключами
#расшифруем h - зашифрованный текст всеми ключами
for i in range(1024):
    key = [int(bit) for bit in bin(i)[2:]]
    key = [0 for i in range(0, 10 - len(key))] + key
    s = "".join(str(x) for x in key)
    res_enc = "".join(str(x) for x in s_des_encrypt(m, key, True))
    res_dec = "".join(str(x) for x in s_des_encrypt(h, key, False))
    m_enc[s] = res_enc
    h_dec[s] = res_dec

print("Всего пар для сравнения =\t", 1 << 20)
sim_key = []
for x in m_enc:
    for y in h_dec:
        if m_enc.get(x) == h_dec.get(y):
            sim_key.append([x, y])
print("The remaining number of key pairs for the plain text=\t", len(sim_key))
count = 0
while len(sim_key) != 1:
    _m = [int(bit) for bit in bin(random.randrange(255))[2:]]
    _m = [0 for i in range(0, 8 - len(_m))] + _m
    _h = s_des_encrypt(s_des_encrypt(_m, k1, True), k2, True)
    tmp_sim_key = []
    for x in sim_key:
        _k1 = [int(bit) for bit in x[0]]
        _k2 = [int(bit) for bit in x[1]]
        res_enc = s_des_encrypt(_m, _k1, True)
        res_dec = s_des_encrypt(_h, _k2, False)
        if res_enc == res_dec:
            tmp_sim_key.append(x)
    sim_key = tmp_sim_key
    count += 1
    print(
        "\nThe remaining number of key pairs for the ",
        count,
        " generated text=\t",
        len(sim_key),
        "\nNew plain_text=\t",
        "".join(str(x) for x in _m),
        "\tNew cipher_text=\t",
        "".join(str(x) for x in _h),
        "\n",
    )
    if count>15:
        if len(sim_key)>1:
            print(
                "Cipher text=\t",
                "".join(str(x) for x in m),
                "\nKey 1=\t",
                "".join(str(x) for x in k1),
                "\nKey 2=\t",
                "".join(str(x) for x in k2),
                "\nDouble S-DES=\t",
                "".join(str(x) for x in h)
            )

            for s in sim_key:
                print("\nGusses key 1=\t",
                s[0],
                "| Eq with k1 ?\t",
                s[0] == "".join(str(x) for x in k1),
                "\nGusses key 2=\t",
                s[1],
                "| Eq with k2 ?\t",
                s[1] == "".join(str(x) for x in k2)
                )
            exit(0)
print(
    "Cipher text=\t",
    "".join(str(x) for x in m),
    "\nKey 1=\t",
    "".join(str(x) for x in k1),
    "\nKey 2=\t",
    "".join(str(x) for x in k2),
    "\nDouble S-DES=\t",
    "".join(str(x) for x in h),
    "\nGusses key 1=\t",
    sim_key[0][0],
    "| Eq with k1 ?\t",
    sim_key[0][0] == "".join(str(x) for x in k1),
    "\nGusses key 2=\t",
    sim_key[0][1],
    "| Eq with k2 ?\t",
    sim_key[0][1] == "".join(str(x) for x in k2),
)