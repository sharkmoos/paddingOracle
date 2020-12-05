# Exploiting the Padding Oracle Attack
#### By Ben Roxbee Cox

# Inroducing the Padding Oracle Attack

Simply put, the padding oracle attack (or oracle padding attack) is an attack on the way in which CBC works. CBC (cipher block chaining) is a mode of operation used by some block ciphers, and was created in 1976. In CBC mode, each block of plaintext is XORed with the previous block of cipher text before being encrypted. The first block is XORed with an IV (initialization vector).

![CBC Mode](/images/cbc2.png)

Diagram of the CBC decryption operation.

There are numerous types of padding Oracle attack, however this project focusses on the AES CBC encryption.

The requirements for a padding oracle attack are simple. The attacker must have access to an Oracle (a server) which freely responds to incoming messages, and will confirm whether or not a message is correctly padded. This in itself tells the attacker something. Additionally, the nature of CBC means that an attacker can expose the details of block n, by manipulating block n-1. The second requirement is having a ciphertext produced **by the oracle being attacked**.

## What is a pad?

In block ciphers, the ciphertext **must** be a multiple of the block size. In AES the block size is 16 bytes, and so the ciphertext will always be a multiple of 16. However, what are the chances of someone's plaintext being exactly 16 bytes? Pretty slim. As a way to resolve this, the cipher needs **padding**. This is essentially extra bytes added onto the plaintext before it is encrypted in order to make it equal 16 bytes. If your plaintext is 10 bytes, there will be 6 bytes of padding; 8 bytes will have 8 bytes of padding and so on. Additionally, the standard for adding padding is to pad each byte with the representation of the number of bytes to be padded. If we go back to our example, a 6 byte pad would be padded with *06 06 06 06 06 06*. A 3 byte pad would be *03 03 03*. This tell us something about the ciphertext, and such a block ending with *06 02 08* is **not** valid. This is not in itself vulnerable, due to the CBC mode the padding would not result in a pre image attack style vulnerability (read about that [here](https://en.wikipedia.org/wiki/Preimage_attack), but it will become important later.

# Attacking the Oracle

So, how is this seemingly small flaw exploited? Maths - Lots of maths, but essentially all an attacker needs to break CBC is to know whether or not a generated cipher text created plaintext with valid padding. (In the working example that will be used, it is very clear whether a ciphertext is valid, but even an API returning 200 for valid padding and 500 if not is enough).

![CBC Mode](/images/cbc.png)

(Refer to the diagram again for a visual understanding)

The attack works by calculating the intermediate state of the decryption for each cipher block. This is the point at which the ciphertext has been decrypted but **not** XORed with the previous cipher block. This attack functions by working *up* from the plaintext rather than *down* from the ciphertext. We can use an algorithm to see why the intermediate state is useful. For the purpose of the explination we will be attacking a 3 block ciphertext (IV + C1 + C2). So to attack C2 we can use C1.

    *I2* : Intermediate state of block 2
    *C1* : Cipher block 1
    *P2* : Plaintext block 2

^    : XOR function (It is important to remember XOR is bidirectional)

    I2 = C1 ^ P2

and therefore

    P2 = C1 ^ I2

So, if we have a some ciphertext from block 1 and some intermediary text from block 2, we can XOR them to get valid block 2 plaintext. C1 is already known to us, it is just part of the 'stolen' ciphertext. Therefor, if we can calculate I2 then we will be able to calculate P2. Now, this attack works *up* - so rather than trying to calculate what I2 is we can use our knowledge of padding to force what I2 will be. So how do we do this? 

Lets say our stolen ciphertext is

    7a786376626e6d6c6b6a686766647361cb20bbc7e34c16603060427d7c77ca31bd5c9b3024d82c1a85ee58ef256975db

In our working example, the ciphertext is 3*16 bytes long: IV+C1+C2 so

    IV = 7a786376626e6d6c6b6a686766647361
    C1 = cb20bbc7e34c16603060427d7c77ca31
    C2 = bd5c9b3024d82c1a85ee58ef256975db

We can pass any ciphertext to the Oracle and find out whether it has valid padding or not, we can exploit this  by crafting a payload C1' (spoken as C1 prime) and pre pending it to C2 from our stolen ciphertext. AES block size is 16 and so to crack byte 16 we should begin by generating random bytes for C1'[1..15], and then set C1'[16] to be 00. We then concatenate C1'+C2 and send that at the Oracle. If it is valid  pad then the plaintext of C2[16] should be 01. Why? Because we are forcing the plaintext of C1' (P2') to have one byte of badding, which must be padded as 01:

If 00 had been valid ciphertext then we could calculate the intermediary value like this

    P2[16] = C1[16] ^ I2[16]

then
    
    I2     = C1'    ^ P2'
    I2     = 00     ^ P2'
    I1     = 00     ^ 01   
    I2     = 01 

If the Oracle tells us our ciphertext is invalid we can change the value of C1'[16] to 01, 02 etc until we get valid ciphertext. In the poc code on [GitHub][https://github.com/sharkmoos/paddingOracle/] we got valid padding for 33 (spoken as three three not 33, it is in hex). So lets put that into our formula!

    I2     = 0x51     ^ 01
    I2     = 0x33

We can do this programmatically in python, rather than manually calculating the values. 

        I2 = 0x51 ^ 0x01

So we now know the final byte of the intermediate state when the plaintext is has a final byte of 01. However our plaintext might not be 01, and so we'll reuse the algorithm to find P2[16] and the ciphertext which we stole

    P2[16] = C1[16] ^ I2[16]
    P2[16] = 0x31   ^ 0x33
           = 0x2  # hex
           = 2    # decimal

So we know that the last byte of our plaintext is 02 - this also suggests that the padding length is 02. If you've been following along doing it with your own code or Oracle, you probably felt like this was a lot of work. This highlights the need for automation.

## Repeat the process.

So, renewed with vigor now that one byte has been cracked, we push onto the next. So in the previous example we decided P2'[16] should equal 01, (1 bit of padding) this time we will manipulate 2 bits, and so each byte of padding should equal 02. This time C1'[1..14] can be random, C1'[15] == 0, and C1'[16] should be made so that P2'[16] == 2. So lets calculate what C'1[16] should be.

    C1'[16] = P2'[16] ^ I2[16]
            = 02      ^ 0x33
            = 0x31    # hex  

To recap, the last two bytes of P2' we are trying to now find should == 02 02. Now repeat the process, changing C1'[15] to be 00,01,02 etc until valid cipher text is found. Once it is found, we can get the plaintext for P2[15] the same way as before. In our working example, D0 (208 in base 10) was valid and so we pipe this into the formula.

    I2[15] = C1'[15] ^ P2'[15] 
           = 0xCA    ^ 02
    I2[15] = 0xC8

and then

    P2[15] = C1[15] ^ I2[15]
           = 0xCA     ^ 0xC8
    P2[15] = 0x2  # hex
           = 2 # decimal

Whilst this may seem a little underwhelming whe you see the trend, it is also useful. Yes - we had to crack 2 bytes without getting **any** plaintext that isn't just padding, and it is highly likely to be upwards of 7 bytes of padding before real plaintext message starts being cracked;but it is also a great sanity check that the process is working. (Again highlights the need for heavy automation). 

## Rinse and repeat

This process can be repeated 16 times as this is the number of bytes in block C2. We would generate random characters for C1'[1..13], C1'[14] == 00 and set C1'[15] and C1'[16] so that P2'[15] and P2'[16] both equal 03. And fuzz the Oracle to find out what C1'[14] must be for it to == 03, and then use it calculate the real plaintext P2[14]. This will work on all block, no matter the length, except block 1. Block one is essentially uncrackable because it was encrypted using the IV which would be unknown to the attacker.

I wrote a program to automate this entire process which you can find [here](https://github.com/sharkmoos/paddingOracle/blob/main/automated.py). It uses connects to the server via a socket and interacts fuzzes the entire block, outputting the plaintext. It should be easy to rework too depending on the task.

This is a good demonstration of why security through obscurity is effective - if the attacker couldn't test whether padding was valid, this attack would fail before it began. I hope you enjoyed reading this article, or failing that found it useful. 
