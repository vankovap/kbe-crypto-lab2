# Lab 2

Solution authors:

- Petra Vaňková (*vankope6@fel.cvut.cz*)
- Martin Hula (*hulamart@fel.cvut.cz*)
- Petr Stejskal (*stejspe7@fel.cvut.cz*)

Language: Python 3

The `main.py` script prints all the answers to stdout.

## Exercise 1: why we do all of this
**Solution:**

`I,(Petra Vaňková, Martin Hula, Petr Stejskal) , understand that cryptography is easy to mess up, and
that I will not carelessly combine pieces of cryptographic ciphers to
encrypt my users' data. I will not write crypto code myself, but defer to
high-level libraries written by experts who took the right decisions for me, like NaCL.`

## Exercise 2: encrypt single-block AES

What is the ciphertext of encrypting the plaintext `90 miles an hour` with the
key `CROSSTOWNTRAFFIC`? Answer in hex.

**Solution:**

Ciphertext is `092fb4b0aa77beddb5e55df37b73faaa`.

## Exercise 3: decrypt single-block AES

What is the decryption of the 16 byte block `fad2b9a02d4f9c850f3828751e8d1565`
with the key `VALLEYSOFNEPTUNE`?

**Solution:**

Original plaintext is `I feel the ocean`.

## Exercise 4: implement PKCS&#35;7 padding

What is the output of `pad("hello")`?

**Solution:**

Output of function is `b'hello\x0b\x0b\x0b\x0b\x0b\x0b\x0b\x0b\x0b\x0b\x0b'`.

## Exercise 5: implement PKCS#7 unpadding

What is the output of `unpad("hello\x0b\x0b\x0b\x0b\x0b\x0b\x0b\x0b\x0b\x0b\x0b")`?

**Solution:**

Output of function is `hello`.

## Exercise 6: implement ECB encryption

What is the encryption of the following plaintext? Use the key `vdchldslghtrturn`. Answer in hex.

    Well, I stand up next to a mountain and I chop it down with the edge of my hand

**Solution:**

Ciphertext is 

    883319258b745592ef20db9dda39b076a84f4955a48ba9caecd1583641cf3acac86acd5e5795de7895fab54481e9d8c3afc179c39412282eb8445ea2450e763df7282998a74baf19887c843b658f8891

## Exercise 7: implement ECB decryption

What is the decryption of the following ECB encoded ciphertext? Use the key `If the mountains`.

    792c2e2ec4e18e9d3a82f6724cf53848
    abb28d529a85790923c94b5c5abc34f5
    0929a03550e678949542035cd669d4c6
    6da25e59a5519689b3b4e11a870e7cea

**Solution:**

Original plaintext is `If the mountains fell in the sea / Let it be, it ain't me`.

## Exercise 8: ECB ciphertext manipulation (cut and paste 1)

1. Have a quick look at the hex file. Can you quickly spot some obvious
   patterns? What fact can you deduce about the song lyrics?
   
   **Solution:**

   `Some lines are completely repeated e.g. line 9 and 21 or lines 2,4,6,8,12.... In a lot of lines there is the second block repeated '0a5f54b2886d308f7ffd76cd41c3e1a9' eg. line 9,16,19...`
   `Song has repeating verses and refrains.`

2. At the end of the file, you can see a 16 byte block "alone"; however, all
   lines of the song lyrics are really 32 bytes long. Can you explain the
   presence of this last 16 byte block? Can you guess the plaintext of this
   block?
   
   **Solution:**
   
   `At first we could think, it is a shorter text, a signature or a motto, but the answer is more obvious. It is an empty line, we often do at the end of files.`

4. Then, decrypt the text with key `TLKNGBTMYGNRTION`. The first line should
   start with "People" -- what is the rest of this line?
   
   **Solution:**
   
   Content of line is `People try to put us d-down`.
   
## Exercise 9: ECB message crafting (cut and paste 2)

2. What is the ciphertext of `welcome("Jim")`? Answer in hex.
   
    **Solution:**
    Ciphertext is `d4d7730a2d4255c88dead80a2ad924f2b114fddb898d7ef8abdfefef30d552863f62b0605102e0186402df7666edcec7`
    
5. Use these blocks (and perhaps other calls to `welcome`) to craft an encrypted
   message whose plaintext starts by `"Your name is "` and finishes with `" and you
   are an admin"`. In your report, write down your crafted ciphertext.
   
   **Solution:**   
   `37a9b711912fb58496097b8f6cc23abe0f07a3c84535a484e76f651644f4c37140b8d021d8079fbc03d6aa56f466423f`

6. Decrypt your encrypted message to make sure it is correct. In your report,
   write the decrypted message.
   
   **Solution:**
   After calling `produce_fake_welcome('Petra')` we get hex output above in 5, after decryption we get
   `Your name is Petra and you are an admin`

7. Could you quickly describe a real-world scenario where this could be a
   security issue?
   
   **Answer:**
   As real-world scenario we can imagine situation, where we send a message via internet. Attacker can catch the message and change the content. 
   Without any manipulation the check mechanism is not possible to find out if message is original or manipulated. It can be a message to internet banking (a transaction request) or in some chat. 

## Exercise 10: ECB decryption (cracking) byte-at-a-time

1. Call hide_secret() with an input containing fifteen times (16-1) the character A: "AAAAAAAAAAAAAAA". In the first block to be encrypted, what will be the last plaintext byte?

    **Answer:**
    `Last character of first block will be first character of secret message, in this situation character 't'`.

- You could continue cracking new bytes, but they will always have the value 1. Why?

    **Answer:**
    `In situation when we crack the last char of secret (plaintext), we decrease count of A chars at the beginning. After that 
    we try to crack next byte, which is one byte of padding with hex value 0x01 (because plaintext moved to left and padding is filled to 16 byte block). We take this byte and concatenate it to the already known secret string. `

    `In the next round we decrease number of As and again concatenate the known secret string with As block. So in the last block we have 15 bytes (known secret plus one byte with 0x01 hex value) and the algorithm again adds 1 byte of padding to last position (0x01). After that the value we always obtain is the same padding byte repeatedly generated by our cracking algorithm.`

- The length of the response to your initial call hide_secret("AAA..AA") will be exactly a + s + 1 where a is the number of A's (between 0 and 15) and s is how many secret bytes you know so far. Why is this true only when the secret is complete?

    **Answer:**
    When the secret is completely reached in formula `a + s + 1`, `a` is equal to `number of A's` in input to hide_secret, 
    `s` is equal `whole known secret length` and `+1` is `one padding byte`. So length of output is corresponding with this formula, 
    when we can say, we have reached whole secret. We name this length as `L`. Why is this true only when the secret is complete? 
    
  - In situation of complete secret, the padding is 1 byte long. Generally we can see that output string from hide_secret() has `shortest length` if padding has 1 byte length.
  - There can be more of these situations when padding length is 1. Such situation is when length of the secret is % 16 == 0.
  - We can create formula for this shortest length of output situations: `a + s + u + 1`,  where `u` is number of uncracked characters.
  - Then it is true that `a + s + u + 1` is equal to formula `a + s + 1` in situation of complete secret.
  - When secret is not complete, `u >= 1` in `a + s + u + 1`, we can see that `a + s + 1` must be lower than length of produced output string.
  - So `a + s + u + 1` equals to `L` only of `u` is zero and this state happens if we have reached the whole secret.
