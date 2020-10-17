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
        raise Exception("Length of the plaintext must be 16 bytes, it is %s bytes.".format(len(x.encode('utf-8'))))
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
        raise Exception("Length of the ciphertext must be 16 bytes, it is %s bytes.".format(len(y.encode('utf-8'))))
    cipher = AES.new(key_bin, AES.MODE_ECB)
    plaintext = cipher.decrypt(data_bin)
    return bin2txt(plaintext)


def pad(x):
    data_bin = txt2bin(x)
    print(len(data_bin))
    pad_length = 16 - (len(data_bin) % 16)
    # pad_string = hex(pad_length).lstrip('0x').rjust(2, '0')
    pad_string = format(pad_length, "x").rjust(2, '0')
    for i in range(pad_length):
        # print(hex2bin(pad_string))
        # print(hex(pad_length).lstrip('0x').rjust(2, '0'))
        data_bin += bytes(hex2bin(pad_string))
    return data_bin


def unpad(y):
    data_bin = txt2bin(y)
    pad_length = data_bin[-1]
    return bin2txt(data_bin[:-pad_length])
    # print(data_bin[-1])


def encrypt_aes_ecb(x, key):
    # output is binary
    padded_data = pad(x)
    cipher_text = ''
    for i in range(len(padded_data) // 16):
        print(padded_data[i*16:(i+1)*16])
        print(len(padded_data[i*16:(i+1)*16]))
        cipher_text += encrypt_aes_block(padded_data[i*16:(i+1)*16], key)
    return cipher_text


def decrypt_aes_ecb(y, key):
    padded_data = hex2bin(y)
    plain_text = ''
    for i in range(len(padded_data) // 16):
        print(padded_data[i*16:(i+1)*16])
        print(len(padded_data[i*16:(i+1)*16]))
        plain_text += decrypt_aes_block(padded_data[i*16:(i+1)*16], key)
    return unpad(plain_text)


if __name__ == '__main__':
    print(encrypt_aes_block('90 miles an hour', 'CROSSTOWNTRAFFIC'))
    #print(encrypt_aes_block('Well, I stand up', 'vdchldslghtrturn'))

    print(decrypt_aes_block('092fb4b0aa77beddb5e55df37b73faaa', 'CROSSTOWNTRAFFIC'))

    print(decrypt_aes_block('fad2b9a02d4f9c850f3828751e8d1565', 'VALLEYSOFNEPTUNE'))

    print(pad('hello'))

    print(unpad("hello\x0b\x0b\x0b\x0b\x0b\x0b\x0b\x0b\x0b\x0b\x0b"))

    print(encrypt_aes_ecb('Well, I stand up next to a mountain and I chop it down with the edge of my hand', 'vdchldslghtrturn'))

    print(decrypt_aes_ecb('792c2e2ec4e18e9d3a82f6724cf53848abb28d529a85790923c94b5c5abc34f50929a03550e678949542035cd669d4c66da25e59a5519689b3b4e11a870e7cea',
                          'If the mountains'))
