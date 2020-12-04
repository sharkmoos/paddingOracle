"""This script, when finished, will fully (and efficiently) crack all but 
the first block of the ciphertext. It utilises the algorithms created in the poc."""
from pwn import *
import server   # To negate the need for socket programming currently
host = "127.0.0.1"
port = 23333
flag = []   # plaintext answer
count = 16  # Bytes in block 1
xor = 1    # Starting value to xor with
i2list = []
count1 = 4  # For slicing
count2 = 2  # For slicing

endCut = 2

cLoco1 = 62 # positions in C1 that is being attacked
cLoco2 = 64

cPointer1 = 0
cPointer2 = 2

"""cipher = "7a786376626e6d6c6b6a686766647361cb20bbc7e34c16603060427d7c77ca31bd5c9b3024d82c1a85ee58ef256975db"  # Cipher text recieved from Oracle
iv  =    "7a786376626e6d6c6b6a686766647361"    # Initialisation vector
oc1 = "cb20bbc7e34c16603060427d7c77ca31"    # Block 1
oc2 = "bd5c9b3024d82c1a85ee58ef256975db"    # Block 2"""
primes = []
valid = []
tail=[]
hexvals = []

for i in range(255):    hexvals.append(i)    # generate all hex values


if __name__ == "__main__":
    p = remote(host,port)
    print(p.recvuntil(b'2. Send your encrypted message.\n'))
    p.sendline(b"1")
    cipher = (p.recvline()).decode("utf-8")
    print("Beginning Attack...")
    c = [cipher[i:i+32] for i in range(0, len(cipher), 32)]
    iv = c[0]
    oc1 = c[1]
    oc2 = c[2]
    for i in hexvals:
        p.recvuntil(b'2. Send your encrypted message.\n')
        p.sendline(b"2")
        p.recvline()
        prime = iv+oc1[:-endCut]+bytes([i]).hex()+''.join(tail)+oc2
        p.sendline(prime.encode())
        #result = server.is_padding_ok(bytes.fromhex(prime))
        result = p.recvline()
        result = result.decode("utf-8")
        if "Invalid" in result:
            pass
        else:
            if prime.strip() != cipher.strip():  # Save new valid pad
                current = prime
    c1 = current[32:64]
    """Some cryptography voodoo for calculating paintext."""
    c1p = int(current[cLoco1:cLoco2], 16)   # Grab the hex from the cipher
    # I2[16] = C1p[16] ^ P2p[16]
    i2 = c1p ^ xor                 # xor with forced value of padding
    #p2[16] = c1[16] ^ I2[16]
    c1i = int(oc1[-cPointer2:], 16)         # Grab original hex value
    p2 = c1i ^ i2
    flag.insert(0, p2)
    # Next step is to calcuate the new C1 prime value
    xor += 1
    i2list.append(i2)
    #c1p[16] = p2p[16] ^ i2[16]
    for i in i2list:    tail.insert(0, bytes([xor ^ i]).hex())  # Store value to be injected into c1p[16]
    #c1p = int(c1p, 16)
    
    endCut += 2
    cLoco1 += -2
    cLoco2 += -2
    cPointer1 += 2
    cPointer2 += 2
    
    while count > 1:

        for i in hexvals:
            p.recvuntil(b'2. Send your encrypted message.\n')
            p.sendline(b"2")
            p.recvline()
            prime = iv+c1[:-endCut]+bytes([i]).hex()+''.join(tail)+oc2
            #result = server.is_padding_ok(bytes.fromhex(prime))
            p.sendline(prime.encode())
            result = p.recvline()
            result = result.decode("utf-8")
            if "Invalid" in result:
                pass
            else:
                current = prime
        tail = []
        """Repeat crypto voodoo"""
        c1p = int(current[cLoco1:cLoco2], 16)   # Grab the hex from the cipher
        # I2[16] = C1p[16] ^ P2p[16]
        i2 = c1p ^ xor                 # xor with forced value of padding
        #p2[16] = c1[16] ^ I2[16]
        c1i = int(oc1[-cPointer2:-cPointer1], 16)         # Grab original hex value
        p2 = c1i ^ i2
        # Next step is to calcuate the new C1 prime value
        xor += 1
        i2list.append(i2)
        flag.insert(0, p2)
        #c1p[16] = p2p[16] ^ i2[16]
        for i in i2list:    tail.insert(0,bytes([xor ^ i]).hex())  # Store value to be injected into c1p[16]
        #c1p = int(c1p, 16)
        endCut += 2
        cLoco1 += -2
        cLoco2 += -2
        cPointer1 += 2
        cPointer2 += 2
        count += -1

for i in flag:
    i = chr(i)
    print(i, end='')