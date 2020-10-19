# Lab 2

## Exercise 1: why we do all of this
`I, <your name here>, understand that cryptography is easy to mess up, and
that I will not carelessly combine pieces of cryptographic ciphers to
encrypt my users' data. I will not write crypto code myself, but defer to
high-level libaries written by experts who took the right decisions for me,
like NaCL.`

## Exercise 2: encrypt single-block AES

What is the ciphertext of encrypting the plaintext `90 miles an hour` with the
key `CROSSTOWNTRAFFIC`? Answer in hex.

Ciphertext is `092fb4b0aa77beddb5e55df37b73faaa`.

## Exercise 3: decrypt single-block AES

What is the decryption of the 16 byte block `fad2b9a02d4f9c850f3828751e8d1565`
with the key `VALLEYSOFNEPTUNE`?

Original plaintext is `I feel the ocean`.

## Exercise 4: implement PKCS&#35;7 padding

What is the output of `pad("hello")`?

Output of function is `b'hello\x0b\x0b\x0b\x0b\x0b\x0b\x0b\x0b\x0b\x0b\x0b'`.

## Exercise 5: implement PKCS#7 unpadding

What is the output of `unpad("hello\x0b\x0b\x0b\x0b\x0b\x0b\x0b\x0b\x0b\x0b\x0b")`?

Output of function is `hello`.

## Exercise 6: implement ECB encryption

What is the encryption of the following plaintext? Use the key `vdchldslghtrturn`. Answer in hex.

    Well, I stand up next to a mountain and I chop it down with the edge of my hand

Ciphertext is 

    883319258b745592ef20db9dda39b076a84f4955a48ba9caecd1583641cf3acac86acd5e5795de7895fab54481e9d8c3afc179c39412282eb8445ea2450e763df7282998a74baf19887c843b658f8891

## Exercise 7: implement ECB decryption

What is the decryption of the following ECB encoded ciphertext? Use the key `If the mountains`.

    792c2e2ec4e18e9d3a82f6724cf53848
    abb28d529a85790923c94b5c5abc34f5
    0929a03550e678949542035cd669d4c6
    6da25e59a5519689b3b4e11a870e7cea

Original plaintext is `If the mountains fell in the sea / Let it be, it ain't me`.

## Exercise 8: ECB ciphertext manipulation (cut and paste 1)

1. Have a quick look at the hex file. Can you quickly spot some obvious
   patterns? What fact can you deduce about the song lyrics?
 
   `Some lines are completly repeated e.g. line 9 and 21 orlines 2,4,6,8,12.... In a lot of lines is repeating same second block '0a5f54b2886d308f7ffd76cd41c3e1a9' eg. line 9,16,19...`
   `Song has repeating verse and refrains.`

2. At the end of the file, you can see a 16 byte block "alone"; however, all
   lines of the song lyrics are really 32 bytes long. Can you explain the
   presence of this last 16 byte block? Can you guess the plaintext of this
   block?
   
   `At the first time we can think, it is some shorter text, signature or motto, but answer is moore obvious. It is empty line, we often do at the end of files.`

4. Then, decrypt the text with key `TLKNGBTMYGNRTION`. The first line should
   start with "People" -- what is the rest of this line?
   
   Content of line is `People try to put us d-down`.
