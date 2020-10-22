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
    if len(data_bin) != 16 or + len(key_bin) != 16:
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
    if len(data_bin) != 16 or + len(key_bin) != 16:
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


def produce_fake_welcome(wantedName):
    orig_cipher = welcome(wantedName)

    # calculate padding length
    orig_cipher_len = len(orig_cipher)
    s = ""
    padding_len = 0
    while True:
        if len(welcome(wantedName+s)) > orig_cipher_len:
            break
        else:
            padding_len += 1
            s = s + "x"

    target_pad = (padding_len + 14) % 16 #an admin is 2 char longer, - 2 = 14 in %16, + 14 because prevent of state target_pad < 0
    target_len = (orig_cipher_len/2) - padding_len + 2 + target_pad

    text_before_change = wantedName + " and you are a"
    text_to_change = "n admin"

    changing_len = len(text_to_change) + target_pad

    # if target_len % 16 = 0, we have to add padding block
    if target_pad == 0:
        target_pad = 16
    # produce source to fake
    source_string = text_before_change+text_to_change
    # padding
    pad_hex = format(target_pad, "x").rjust(2, '0')
    source_padding_hex = ""
    for i in range(0, target_pad):
        source_padding_hex += pad_hex

    # final source in hex
    source_string_hex = txt2hex(source_string) + source_padding_hex

    src_hex_len = len(source_string_hex)
    fake_output = ""
    first_byte = src_hex_len - (changing_len * 2)  # len in bytes, we count hex digit

    # encrypt block in welcome function
    for i in range(0, int(src_hex_len/32)):
        start_block = i * 32 + (src_hex_len % 32)
        end_block = (i + 1) * 32 + (src_hex_len % 32)
        if first_byte < end_block:
            block = source_string_hex[start_block : end_block]
            in2 = welcome(hex2txt("000000" + block))
            fake_output += in2[32:64]

    orig_block_len = target_len - changing_len
    num_orig_block = int(orig_block_len / 16)
    fake_welcome = orig_cipher[0:num_orig_block*32]+fake_output

    print("Decrypt test")
    print(fake_welcome)
    print(bin2txt(decrypt_aes_ecb(fake_welcome, 'RIDERSONTHESTORM')))


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
                    if int(secret_key, 16) == 1:
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
    print("== Exercise 1 ==")
    print("I, Petra Vankova, understand that cryptography is easy to mess up,\n",
          "and that I will not carelessly combine pieces of cryptographic ciphers \n",
          "to encrypt my users' data. I will not write non-study-purpose crypto \n"
          "code myself, but defer to high-level libraries written by experts who \n"
          "took the right decisions for me, like NaCL.", "\n")

    # Exercise 2
    print("== Exercise 2 ==")
    print(encrypt_aes_block('90 miles an hour', 'CROSSTOWNTRAFFIC'), "\n")

    # Exercise 3
    print("== Exercise 3 ==")
    print(decrypt_aes_block('092fb4b0aa77beddb5e55df37b73faaa', 'CROSSTOWNTRAFFIC'))

    print(decrypt_aes_block('fad2b9a02d4f9c850f3828751e8d1565', 'VALLEYSOFNEPTUNE'), "\n")

    # Exercise 4
    print("== Exercise 4 ==")
    print(pad('hello'), "\n")

    # Exercise 5
    print("== Exercise 5 ==")
    unpadded = bin2txt(unpad("hello\x0b\x0b\x0b\x0b\x0b\x0b\x0b\x0b\x0b\x0b\x0b"))
    print(unpadded, "\n")

    # Exercise 6
    print("== Exercise 6 ==")
    print(encrypt_aes_ecb('Well, I stand up next to a mountain and I chop it down with the edge of my hand', 'vdchldslghtrturn'), "\n")

    # Exercise 7
    print("== Exercise 7 ==")
    plaintext = decrypt_aes_ecb('792c2e2ec4e18e9d3a82f6724cf53848abb28d529a85790923c94b5c5abc34f50929a03550e678949542035cd669d4c66da25e59a5519689b3b4e11a870e7cea',
                          'If the mountains')
    print(bin2txt(plaintext), "\n")

    # Exercise 8
    print("== Exercise 8 ==")
    with open("text1.hex", "r") as file:
        data = file.read().replace('\n','')
        order_data = swap_lines(data, 32, 0, 2)
        plaintext = decrypt_aes_ecb(order_data, 'TLKNGBTMYGNRTION')
        print(bin2txt(plaintext).split('\n')[0], "\n")

    # Exercise 9
    print("== Exercise 9 ==")
    print(welcome("Jim"))
    print(welcome("Jim" + hex2txt("10101010101010101010101010101010")))
    print(welcome("Jim" + "you are admin"))
    print("--")
    produce_fake_welcome("Petra")
    print("--", "\n")

    # Exercise 10
    print("== Exercise 10 ==")
    print(hide_secret('just listen find the magic key'))
    print("Secret: ", find_secret())
