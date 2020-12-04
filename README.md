# paddingOracle
## Ben Roxbee Cox

This project contains various files.

### Server.py
This file contains the "Oracle" that will be exploited. The "attacker" would not nessessarily need this source code in order to exploit the Oracle, however it is useful in order to confirm that AES CBC encryption is being used.

### poc.py
The poc file is essentially a typed out way of how the attack can be exploited by hand, with no code efficiency. This was written whilst learning/testing the attack and so it is sparadic and illogical. However, it can be useful to read in order to visualise how the attack works.

### automated.py

The automated.py is an exploit program in its own right, it uses python sockets to connect to the remote target and uses exploits the padding oracle attack. Currently it only decrypts block 2 however when finished it will crack all except block 1 (which in uncrackable through the Padding Oracle method). You'll just have to hope its a useless intoduciton such as "Useless intro to fill block 1".
