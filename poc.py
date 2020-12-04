"""This script is written as a half way point. Almost a proof of concept for what may become 
a full socket utilised driven cracking program.It is over-commented and lacking in proper automation methods."""
import server   # To negate the need for socket programming currently
flag = []   # plaintext answer
count = 16  # Bytes in block 1
xor = 1    # Starting value to xor with
i2list = []
count1 = 4  # For slicing
count2 = 2  # For slicing

cLoco1 = 62 # positions in C1 that is being attacked
cLoco2 = 64
orginal = "7a786376626e6d6c6b6a686766647361711680b1aa3ac967f3fc08df5ef1dcfcf0eb73cd073026a8f4fa30582e749e0d"
iv  = "7a786376626e6d6c6b6a686766647361"    # Initialisation vector
oc1 = "711680b1aa3ac967f3fc08df5ef1dcfc"  
oc2 = "f0eb73cd073026a8f4fa30582e749e0d"
primes = []
valid = []
tail=[]
"""First stage is done differently due to nature of finding first pad."""
for i in range(255):
    primes.append(iv+oc1[:-2]+bytes([i]).hex()+oc2) # Generate list of attempts

for i in primes:
    result = server.is_padding_ok(bytes.fromhex(i)) # Gather results
    if "Invalid" in result:
        pass    # Ignore errors
    else:
        print(f"Trying with {i}\n\tgives: {server.is_padding_ok(bytes.fromhex(i))}") # Record valid
        if i != orginal: # Save new valid pad
            current = i

#========================================== # Never EVER do this in real programming scripts
"""Some cryptography voodoo for calculating paintext."""

c1p = int(current[62:64], 16)   # Grab the hex from the cipher
print(c1p)                      # 243
# I2[16] = C1p[16] ^ P2p[16]
i2 = c1p ^ 0x01                 # xor with forced value of padding
print(f"i2 is {i2}")
#p2[16] = c1[16] ^ I2[16]
c1i = int(oc1[-2:], 16)         # Grab original hex value
p2 = c1i ^ i2
print(f"The values so far: {p2} ")
# Next step is to calcuate the new C1 prime value
xor += 1
i2list = []
i2list.append(i2)
print(f"xor is {xor}")
#c1p[16] = p2p[16] ^ i2[16]
for i in i2list:    tail.append(bytes([xor ^ i]).hex())  # Store value to be injected into c1p[16]
print(f"tail is {tail}")
#c1p = int(c1p, 16)

#==============================================
hexvals = [] 
c1 = current[32:64]
for i in range(255):    hexvals.append(i)    # generate all hex values
#primes.append(iv+oc1[:-2]+bytes([i]).hex()+oc2)
for i in hexvals:
    prime = iv+c1[:-4]+bytes([i]).hex()+''.join(tail)+oc2
    result = server.is_padding_ok(bytes.fromhex(prime))
    if "Invalid" in result:
        pass
    else:
        current = prime
        print(f"Found valid pad {i} using prime: \t {prime}")
tail = []
# Repeat crypto voodoo
c1p = int(current[60:62], 16)   # Grab the hex from the cipher
print(c1p)                      # 243
# I2[16] = C1p[16] ^ P2p[16]
i2 = c1p ^ xor                 # xor with forced value of padding
print(f"i2 is {i2}")
#p2[16] = c1[16] ^ I2[16]
c1i = int(oc1[-4:-2], 16)         # Grab original hex value
p2 = c1i ^ i2
print(f"The values so far: {p2} ")
# Next step is to calcuate the new C1 prime value
xor += 1
i2list.append(i2)
print(f"xor is {xor}")
#c1p[16] = p2p[16] ^ i2[16]
for i in i2list:    tail.insert(0,bytes([xor ^ i]).hex())  # Store value to be injected into c1p[16]
print(f"tail is {tail}")
#c1p = int(c1p, 16)
#====================================================
for i in hexvals:
    prime = iv+c1[:-6]+bytes([i]).hex()+''.join(tail)+oc2
    result = server.is_padding_ok(bytes.fromhex(prime))
    if "Invalid" in result:
        pass
    else:
        current = prime
        print(f"Found valid pad {i} using prime: \t {prime}")
tail = []
# Repeat crypto voodoo
c1p = int(current[58:60], 16)   # Grab the hex from the cipher
print(f"The value of C prime 1 is {c1p}")                      # 243
# I2[16] = C1p[16] ^ P2p[16]
i2 = c1p ^ xor                 # xor with forced value of padding
print(f"i2 is {i2}")
#p2[16] = c1[16] ^ I2[16]
c1i = int(oc1[-6:-4], 16)         # Grab original hex value
p2 = c1i ^ i2
print(f"The values so far: {p2} ")
# Next step is to calcuate the new C1 prime value
xor += 1
i2list.append(i2)
print(f"xor is {xor}")
#c1p[16] = p2p[16] ^ i2[16]
for i in i2list:    tail.insert(0,bytes([xor ^ i]).hex())  # Store value to be injected into c1p[16]
print(f"tail is {tail}")
#c1p = int(c1p, 16)

#====================================================
for i in hexvals:
    prime = iv+c1[:-8]+bytes([i]).hex()+''.join(tail)+oc2
    result = server.is_padding_ok(bytes.fromhex(prime))
    if "Invalid" in result:
        pass
    else:
        current = prime
        print(f"Found valid pad {i} using prime: \t {prime}")
tail = []
# Repeat crypto voodoo
c1p = int(current[56:58], 16)   # Grab the hex from the cipher
print(f"The value of C prime 1 is {c1p}")                      # 243
# I2[16] = C1p[16] ^ P2p[16]
i2 = c1p ^ xor                 # xor with forced value of padding
print(f"i2 is {i2}")
#p2[16] = c1[16] ^ I2[16]
c1i = int(oc1[-8:-6], 16)         # Grab original hex value
p2 = c1i ^ i2
print(f"The values so far: {p2} ")
# Next step is to calcuate the new C1 prime value
xor += 1
i2list.append(i2)
print(f"xor is {xor}")
#c1p[16] = p2p[16] ^ i2[16]
for i in i2list:    tail.insert(0,bytes([xor ^ i]).hex())  # Store value to be injected into c1p[16]
print(f"tail is {tail}")
#c1p = int(c1p, 16)
#===========================================================
#====================================================
for i in hexvals:
    prime = iv+c1[:-10]+bytes([i]).hex()+''.join(tail)+oc2
    result = server.is_padding_ok(bytes.fromhex(prime))
    if "Invalid" in result:
        pass
    else:
        current = prime
        print(f"Found valid pad {i} using prime: \t {prime}")
tail = []
# Repeat crypto voodoo
c1p = int(current[54:56], 16)   # Grab the hex from the cipher
print(f"The value of C prime 1 is {c1p}")                      # 243
# I2[16] = C1p[16] ^ P2p[16]
i2 = c1p ^ xor                 # xor with forced value of padding
print(f"i2 is {i2}")
#p2[16] = c1[16] ^ I2[16]
c1i = int(oc1[-10:-8], 16)         # Grab original hex value
p2 = c1i ^ i2
print(f"The values so far: {p2} ")
# Next step is to calcuate the new C1 prime value
xor += 1
i2list.append(i2)
print(f"xor is {xor}")
#c1p[16] = p2p[16] ^ i2[16]
for i in i2list:    tail.insert(0,bytes([xor ^ i]).hex())  # Store value to be injected into c1p[16]
print(f"tail is {tail}")
#c1p = int(c1p, 16)
#====================================================
for i in hexvals:
    prime = iv+c1[:-12]+bytes([i]).hex()+''.join(tail)+oc2
    result = server.is_padding_ok(bytes.fromhex(prime))
    if "Invalid" in result:
        pass
    else:
        current = prime
        print(f"Found valid pad {i} using prime: \t {prime}")
tail = []
# Repeat crypto voodoo
c1p = int(current[52:54], 16)   # Grab the hex from the cipher
print(f"The value of C prime 1 is {c1p}")                      # 243
# I2[16] = C1p[16] ^ P2p[16]
i2 = c1p ^ xor                 # xor with forced value of padding
print(f"i2 is {i2}")
#p2[16] = c1[16] ^ I2[16]
c1i = int(oc1[-12:-10], 16)         # Grab original hex value
p2 = c1i ^ i2
print(f"The values so far: {p2} ")
# Next step is to calcuate the new C1 prime value
xor += 1
i2list.append(i2)
print(f"xor is {xor}")
#c1p[16] = p2p[16] ^ i2[16]
for i in i2list:    tail.insert(0,bytes([xor ^ i]).hex())  # Store value to be injected into c1p[16]
print(f"tail is {tail}")
#c1p = int(c1p, 16)
#====================================================
for i in hexvals:
    prime = iv+c1[:-14]+bytes([i]).hex()+''.join(tail)+oc2
    result = server.is_padding_ok(bytes.fromhex(prime))
    if "Invalid" in result:
        pass
    else:
        current = prime
        print(f"Found valid pad {i} using prime: \t {prime}")
tail = []
# Repeat crypto voodoo
c1p = int(current[50:52], 16)   # Grab the hex from the cipher
print(f"The value of C prime 1 is {c1p}")                      # 243
# I2[16] = C1p[16] ^ P2p[16]
i2 = c1p ^ xor                 # xor with forced value of padding
print(f"i2 is {i2}")
#p2[16] = c1[16] ^ I2[16]
c1i = int(oc1[-14:-12], 16)         # Grab original hex value
p2 = c1i ^ i2
print(f"The values so far: {p2} ")
# Next step is to calcuate the new C1 prime value
xor += 1
i2list.append(i2)
print(f"xor is {xor}")
#c1p[16] = p2p[16] ^ i2[16]
for i in i2list:    tail.insert(0,bytes([xor ^ i]).hex())  # Store value to be injected into c1p[16]
print(f"tail is {tail}")
#c1p = int(c1p, 16)
#====================================================
for i in hexvals:
    prime = iv+c1[:-16]+bytes([i]).hex()+''.join(tail)+oc2
    result = server.is_padding_ok(bytes.fromhex(prime))
    if "Invalid" in result:
        pass
    else:
        current = prime
        print(f"Found valid pad {i} using prime: \t {prime}")
tail = []
# Repeat crypto voodoo
c1p = int(current[48:50], 16)   # Grab the hex from the cipher
print(f"The value of C prime 1 is {c1p}")                      # 243
# I2[16] = C1p[16] ^ P2p[16]
i2 = c1p ^ xor                 # xor with forced value of padding
print(f"i2 is {i2}")
#p2[16] = c1[16] ^ I2[16]
c1i = int(oc1[-16:-14], 16)         # Grab original hex value
p2 = c1i ^ i2
print(f"The values so far: {p2} ")
# Next step is to calcuate the new C1 prime value
xor += 1
i2list.append(i2)
print(f"xor is {xor}")
#c1p[16] = p2p[16] ^ i2[16]
for i in i2list:    tail.insert(0,bytes([xor ^ i]).hex())  # Store value to be injected into c1p[16]
print(f"tail is {tail}")
#c1p = int(c1p, 16)

#====================================================
for i in hexvals:
    prime = iv+c1[:-18]+bytes([i]).hex()+''.join(tail)+oc2
    result = server.is_padding_ok(bytes.fromhex(prime))
    if "Invalid" in result:
        pass
    else:
        current = prime
        print(f"Found valid pad {i} using prime: \t {prime}")
tail = []
# Repeat crypto voodoo
c1p = int(current[46:48], 16)   # Grab the hex from the cipher
print(f"The value of C prime 1 is {c1p}")                      # 243
# I2[16] = C1p[16] ^ P2p[16]
i2 = c1p ^ xor                 # xor with forced value of padding
print(f"i2 is {i2}")
#p2[16] = c1[16] ^ I2[16]
c1i = int(oc1[-18:-16], 16)         # Grab original hex value
p2 = c1i ^ i2
print(f"The values so far: {p2} ")
# Next step is to calcuate the new C1 prime value
xor += 1
i2list.append(i2)
print(f"xor is {xor}")
#c1p[16] = p2p[16] ^ i2[16]
for i in i2list:    tail.insert(0,bytes([xor ^ i]).hex())  # Store value to be injected into c1p[16]
print(f"tail is {tail}")
#c1p = int(c1p, 16)
#====================================================
for i in hexvals:
    prime = iv+c1[:-20]+bytes([i]).hex()+''.join(tail)+oc2
    result = server.is_padding_ok(bytes.fromhex(prime))
    if "Invalid" in result:
        pass
    else:
        current = prime
        print(f"Found valid pad {i} using prime: \t {prime}")
tail = []
# Repeat crypto voodoo
c1p = int(current[44:46], 16)   # Grab the hex from the cipher
print(f"The value of C prime 1 is {c1p}")                      # 243
# I2[16] = C1p[16] ^ P2p[16]
i2 = c1p ^ xor                 # xor with forced value of padding
print(f"i2 is {i2}")
#p2[16] = c1[16] ^ I2[16]
c1i = int(oc1[-20:-18], 16)         # Grab original hex value
p2 = c1i ^ i2
print(f"The values so far: {p2} ")
# Next step is to calcuate the new C1 prime value
xor += 1
i2list.append(i2)
print(f"xor is {xor}")
#c1p[16] = p2p[16] ^ i2[16]
for i in i2list:    tail.insert(0,bytes([xor ^ i]).hex())  # Store value to be injected into c1p[16]
print(f"tail is {tail}")
#c1p = int(c1p, 16)
#====================================================
for i in hexvals:
    prime = iv+c1[:-22]+bytes([i]).hex()+''.join(tail)+oc2
    result = server.is_padding_ok(bytes.fromhex(prime))
    if "Invalid" in result:
        pass
    else:
        current = prime
        print(f"Found valid pad {i} using prime: \t {prime}")
tail = []
# Repeat crypto voodoo
c1p = int(current[42:44], 16)   # Grab the hex from the cipher
print(f"The value of C prime 1 is {c1p}")                      # 243
# I2[16] = C1p[16] ^ P2p[16]
i2 = c1p ^ xor                 # xor with forced value of padding
print(f"i2 is {i2}")
#p2[16] = c1[16] ^ I2[16]
c1i = int(oc1[-22:-20], 16)         # Grab original hex value
p2 = c1i ^ i2
print(f"The values so far: {p2} ")
# Next step is to calcuate the new C1 prime value
xor += 1
i2list.append(i2)
print(f"xor is {xor}")
#c1p[16] = p2p[16] ^ i2[16]
for i in i2list:    tail.insert(0,bytes([xor ^ i]).hex())  # Store value to be injected into c1p[16]
print(f"tail is {tail}")
#c1p = int(c1p, 16)
#====================================================
for i in hexvals:
    prime = iv+c1[:-24]+bytes([i]).hex()+''.join(tail)+oc2
    result = server.is_padding_ok(bytes.fromhex(prime))
    if "Invalid" in result:
        pass
    else:
        current = prime
        print(f"Found valid pad {i} using prime: \t {prime}")
tail = []
# Repeat crypto voodoo
c1p = int(current[40:42], 16)   # Grab the hex from the cipher
print(f"The value of C prime 1 is {c1p}")                      # 243
# I2[16] = C1p[16] ^ P2p[16]
i2 = c1p ^ xor                 # xor with forced value of padding
print(f"i2 is {i2}")
#p2[16] = c1[16] ^ I2[16]
c1i = int(oc1[-24:-22], 16)         # Grab original hex value
p2 = c1i ^ i2
print(f"The values so far: {p2} ")
# Next step is to calcuate the new C1 prime value
xor += 1
i2list.append(i2)
print(f"xor is {xor}")
#c1p[16] = p2p[16] ^ i2[16]
for i in i2list:    tail.insert(0,bytes([xor ^ i]).hex())  # Store value to be injected into c1p[16]
print(f"tail is {tail}")
#c1p = int(c1p, 16)
#====================================================
for i in hexvals:
    prime = iv+c1[:-26]+bytes([i]).hex()+''.join(tail)+oc2
    result = server.is_padding_ok(bytes.fromhex(prime))
    if "Invalid" in result:
        pass
    else:
        current = prime
        print(f"Found valid pad {i} using prime: \t {prime}")
tail = []
# Repeat crypto voodoo
c1p = int(current[38:40], 16)   # Grab the hex from the cipher
print(f"The value of C prime 1 is {c1p}")                      # 243
# I2[16] = C1p[16] ^ P2p[16]
i2 = c1p ^ xor                 # xor with forced value of padding
print(f"i2 is {i2}")
#p2[16] = c1[16] ^ I2[16]
c1i = int(oc1[-26:-24], 16)         # Grab original hex value
p2 = c1i ^ i2
print(f"The values so far: {p2} ")
# Next step is to calcuate the new C1 prime value
xor += 1
i2list.append(i2)
print(f"xor is {xor}")
#c1p[16] = p2p[16] ^ i2[16]
for i in i2list:    tail.insert(0,bytes([xor ^ i]).hex())  # Store value to be injected into c1p[16]
print(f"tail is {tail}")
#c1p = int(c1p, 16)
#====================================================
for i in hexvals:
    prime = iv+c1[:-28]+bytes([i]).hex()+''.join(tail)+oc2
    result = server.is_padding_ok(bytes.fromhex(prime))
    if "Invalid" in result:
        pass
    else:
        current = prime
        print(f"Found valid pad {i} using prime: \t {prime}")
tail = []
# Repeat crypto voodoo
c1p = int(current[36:38], 16)   # Grab the hex from the cipher
print(f"The value of C prime 1 is {c1p}")                      # 243
# I2[16] = C1p[16] ^ P2p[16]
i2 = c1p ^ xor                 # xor with forced value of padding
print(f"i2 is {i2}")
#p2[16] = c1[16] ^ I2[16]
c1i = int(oc1[-28:-26], 16)         # Grab original hex value
p2 = c1i ^ i2
print(f"The values so far: {p2} ")
# Next step is to calcuate the new C1 prime value
xor += 1
i2list.append(i2)
print(f"xor is {xor}")
#c1p[16] = p2p[16] ^ i2[16]
for i in i2list:    tail.insert(0,bytes([xor ^ i]).hex())  # Store value to be injected into c1p[16]
print(f"tail is {tail}")
#c1p = int(c1p, 16)

#====================================================
for i in hexvals:
    prime = iv+c1[:-30]+bytes([i]).hex()+''.join(tail)+oc2
    result = server.is_padding_ok(bytes.fromhex(prime))
    if "Invalid" in result:
        pass
    else:
        current = prime
        print(f"Found valid pad {i} using prime: \t {prime}")
tail = []
# Repeat crypto voodoo
c1p = int(current[34:36], 16)   # Grab the hex from the cipher
print(f"The value of C prime 1 is {c1p}")                      # 243
# I2[16] = C1p[16] ^ P2p[16]
i2 = c1p ^ xor                 # xor with forced value of padding
print(f"i2 is {i2}")
#p2[16] = c1[16] ^ I2[16]
c1i = int(oc1[-30:-28], 16)         # Grab original hex value
p2 = c1i ^ i2
print(f"The values so far: {p2} ")
# Next step is to calcuate the new C1 prime value
xor += 1
i2list.append(i2)
print(f"xor is {xor}")
#c1p[16] = p2p[16] ^ i2[16]
for i in i2list:    tail.insert(0,bytes([xor ^ i]).hex())  # Store value to be injected into c1p[16]
print(f"tail is {tail}")
#c1p = int(c1p, 16)
#====================================================
for i in hexvals:
    prime = iv+c1[:-32]+bytes([i]).hex()+''.join(tail)+oc2
    result = server.is_padding_ok(bytes.fromhex(prime))
    if "Invalid" in result:
        pass
    else:
        current = prime
        print(f"Found valid pad {i} using prime: \t {prime}")
tail = []
# Repeat crypto voodoo
c1p = int(current[32:34], 16)   # Grab the hex from the cipher
print(f"The value of C prime 1 is {c1p}")                      # 243
# I2[16] = C1p[16] ^ P2p[16]
i2 = c1p ^ xor                 # xor with forced value of padding
print(f"i2 is {i2}")
#p2[16] = c1[16] ^ I2[16]
c1i = int(oc1[-32:-30], 16)         # Grab original hex value
p2 = c1i ^ i2
print(f"The values so far: {p2} ")
# Next step is to calcuate the new C1 prime value
xor += 1
i2list.append(i2)
print(f"xor is {xor}")
#c1p[16] = p2p[16] ^ i2[16]
for i in i2list:    tail.insert(0,bytes([xor ^ i]).hex())  # Store value to be injected into c1p[16]
print(f"tail is {tail}")
#c1p = int(c1p, 16)
#====================================================
