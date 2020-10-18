from Crypto.Cipher import AES


def bin2txt(value):
    return value.decode('utf-8')


def bin2hex(value):
    return value.hex()


def txt2bin(value):
    return value.encode('utf-8')


def hex2bin(value):
    return bytearray.fromhex(value)


def hex2txt(value):
    return bytes.fromhex(value).decode('utf-8')


def txt2hex(value):
    return txt2bin(value).hex()


def encrypt_aes_block(x, key):
    if type(x) is str:
        data_bin = txt2bin(x)
    else:
        data_bin = x
    key_bin = txt2bin(key)
    if len(data_bin) + len(key_bin) != 32:
        raise Exception("Length of the plaintext must be 16 bytes, it is {} bytes.".format(len(x.encode('utf-8'))))
    cipher = AES.new(key_bin, AES.MODE_ECB)
    ciphertext = cipher.encrypt(data_bin)
    return bin2hex(ciphertext)


def decrypt_aes_block(y, key):
    if type(y) is str:
        data_bin = hex2bin(y)
    else:
        data_bin = y
    key_bin = txt2bin(key)
    if len(data_bin) + len(key_bin) != 32:
        raise Exception("Length of the ciphertext must be 16 bytes, it is {} bytes.".format(len(y.encode('utf-8'))))
    cipher = AES.new(key_bin, AES.MODE_ECB)
    plaintext = cipher.decrypt(data_bin)
    return bin2txt(plaintext)


def pad(x):
    if type(x) is str:
        data_bin = txt2bin(x)
    else:
        data_bin = x
    pad_length = 16 - (len(data_bin) % 16)
    pad_string = format(pad_length, "x").rjust(2, '0')
    for i in range(pad_length):
        data_bin += bytes(hex2bin(pad_string))
    return data_bin


def unpad(y):
    data_bin = txt2bin(y)
    pad_length = data_bin[-1]
    return data_bin[:-pad_length]


def encrypt_aes_ecb(x, key):
    # output is binary
    padded_data = pad(x)
    cipher_text = ''
    for i in range(len(padded_data) // 16):
        cipher_text += encrypt_aes_block(padded_data[i*16:(i+1)*16], key)
    return cipher_text


def decrypt_aes_ecb(y, key):
    padded_data = hex2bin(y)
    plain_text = ''
    for i in range(len(padded_data) // 16):
        plain_text += decrypt_aes_block(padded_data[i*16:(i+1)*16], key)
    return unpad(plain_text)


def swap_lines(data, line_length, line1, line2):
    line_length *= 2
    split_data = [data[i:i + line_length] for i in range(0, len(data), line_length)]
    min_index, max_index = min(line1, line2), max(line1, line2)
    swapped_data = split_data[:min_index]
    swapped_data.append(split_data[max_index])
    swapped_data.extend(split_data[min_index+1:max_index])
    swapped_data.append(split_data[min_index])
    swapped_data.extend(split_data[max_index+1:])
    return ''.join(swapped_data)


def welcome(name):
    plaintext = 'Your name is {} and you are a user'.format(name)
    ciphertext = encrypt_aes_ecb(plaintext, 'RIDERSONTHESTORM')
    return ciphertext


def hide_secret(x):
    if type(x) is str:
        x = txt2bin(x)
    SECRET = "this should stay secret"
    plaintext = x + txt2bin(SECRET)
    ciphertext = encrypt_aes_ecb(plaintext, 'COOL T MAGIC KEY')
    return ciphertext


def get_secret_char(secret, block, position, letter):
    length = 16 - position
    x = ''
    for _ in range(0,length-1):
        x += letter
    hidden_secret = hide_secret(x)
    secret_char = hidden_secret[block*30:block*32]
    candidates = []
    for i in range(0x00, 0x7f):
        candidate = hex(i).lstrip('0x').rjust(2, '0')
        plaintext = hex2bin(txt2hex(x + secret) + candidate)
        ciphertext = hide_secret(plaintext)
        candidate_encrypt = ciphertext[block*30:block*32]
        if candidate_encrypt == secret_char:
            candidates.append(candidate)
    if len(candidates) > 1:
        return False, None
    else:
        return True, candidates[0]


def find_secret():
    secret = ''
    block = 1
    while True:
        end = False
        for i in range(0,16):
            found = False
            letter = 0x41
            while not found:
                found, secret_key = get_secret_char(secret, block, i, chr(letter))
                if found:
                    if int(secret_key,16) < 32:
                        end = True
                        if end:
                            break
                    secret += hex2txt(secret_key)
                    break
                if letter + 1 > 128:
                    raise Exception("Non ASCII character")
                else:
                    letter += 1
            if end:
                break
        if end:
            break
        block += 1
    return secret


if __name__ == '__main__':
    # Exercise 1
    print("I, Petra Vankova, understand that cryptography is easy to mess up,\n",
          "and that I will not carelessly combine pieces of cryptographic ciphers \n",
          "to encrypt my users' data. I will not write non-study-purpose crypto \n"
          "code myself, but defer to high-level libraries written by experts who \n"
          "took the right decisions for me, like NaCL.")

    # Exercise 2
    print(encrypt_aes_block('90 miles an hour', 'CROSSTOWNTRAFFIC'))

    # Exercise 3
    print(decrypt_aes_block('092fb4b0aa77beddb5e55df37b73faaa', 'CROSSTOWNTRAFFIC'))

    print(decrypt_aes_block('fad2b9a02d4f9c850f3828751e8d1565', 'VALLEYSOFNEPTUNE'))

    # Exercise 4
    print(pad('hello'))

    # Exercise 5
    unpadded = bin2txt(unpad("hello\x0b\x0b\x0b\x0b\x0b\x0b\x0b\x0b\x0b\x0b\x0b"))
    print(unpadded)

    # Exercise 6
    print(encrypt_aes_ecb('Well, I stand up next to a mountain and I chop it down with the edge of my hand', 'vdchldslghtrturn'))

    # Exercise 7
    plaintext = decrypt_aes_ecb('792c2e2ec4e18e9d3a82f6724cf53848abb28d529a85790923c94b5c5abc34f50929a03550e678949542035cd669d4c66da25e59a5519689b3b4e11a870e7cea',
                          'If the mountains')
    print(bin2txt(plaintext))

    # Exercise 8
    with open("text1.hex", "r") as file:
        data = file.read().replace('\n','')
        order_data = swap_lines(data, 32, 0, 2)
        plaintext = decrypt_aes_ecb(order_data, 'TLKNGBTMYGNRTION')
        print(bin2txt(plaintext).split('\n')[0])

    # Exercise 9
    print(welcome("Jim"))
    print(welcome("Jim" + hex2txt("10101010101010101010101010101010")))
    print(welcome(hex2txt('000000')))
    print(welcome("JimPetra and " + hex2txt("000000000000")))
    print(welcome("Jimyou are an admin"))
    print(bin2txt(decrypt_aes_ecb('75e01419cbb5065fd1c7fcc1091facfc46a36e9148f3a7277de22bd34e48ddd87edb62ceff6a92e3a59029a06e5e622b4e9eb1df207c25bebdcfc57385251689', 'RIDERSONTHESTORM')))

    # Exercise 10
    print(hide_secret('just listen find the magic key'))
    print("Secret: ", find_secret())
