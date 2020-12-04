import server
primes = []
valid = []

iv = "7a786376626e6d6c6b6a686766647361"
c1 = "711680b1aa3ac967f3fc08df5ef1dcfc"
c2 = "f0eb73cd073026a8f4fa30582e749e0d"

for i in range(255):
    primes.append(iv+c1[:-2]+bytes([i]).hex()+c2)

for i in primes:
    result = server.is_padding_ok(bytes.fromhex(i))
    if "Invalid" in result:
        pass
    else:
        #print(f"Trying with {i}\n\tgives: {server.is_padding_ok(bytes.fromhex(i))}")
        valid.append(i)
# ===========================================================

c1 = "711680b1aa3ac967f3fc08df5ef100f0"
primes = []
for i in range(255):
    primes.append(iv+c1[:-4]+bytes([i]).hex()+c1[-2:]+c2)

for i in primes:
    result = server.is_padding_ok(bytes.fromhex(i))
    if "Invalid" in result:
        pass
    else:
       # print(f"Trying with {i}\n\tgives: {server.is_padding_ok(bytes.fromhex(i))}")
        valid.append(i)

#===================================================================

c1 = "711680b1aa3ac967f3fc08df5ef1d1f0"
primes = []
for i in range(255):
    primes.append(iv+c1[:-6]+bytes([i]).hex()+c1[-4:]+c2)

for i in primes:
    result = server.is_padding_ok(bytes.fromhex(i))
    if "Invalid" in result:
        pass
    else:
        print(f"Trying with {i}\n\tgives: {server.is_padding_ok(bytes.fromhex(i))}")
        valid.append(i)
