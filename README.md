# Quark
This is a python implementation for the Quark hash function.

### What is Quark ?

Quark is a cryptographic hash function (family). It was designed by Jean-Philippe Aumasson, Luca Henzen, Willi Meier and María Naya-Plasencia.

Quark was created because of the expressed need by application designers (notably for implementing RFID protocols) for a lightweight cryptographic hash function. The SHA-3 NIST hash function competition concerned general-purpose designs and focused on software performance.

Quark is a lightweight hash function, based on a single security level and on the sponge construction, to minimize memory requirements. Inspired by the lightweight ciphers Grain and KATAN, the hash function family Quark is composed of the three instances u-Quark, d-Quark, and s-Quark. Hardware benchmarks show that Quark compares well to previous lightweight hashes.

### Implementation

This is an implementation for the Quark hash family that includes the 3 instances : u-Quark, d-Quark and s-Quark.

Every instance is a python class that has a method called "keyed_hash()" and it takes as inputs the message and the key and the output representation type (hex or binary).


#### Example

In your file, you can import the Quark.py file, create an object of one of the classes and then use the hash function :
```python
import QUARK
# some code...
object = QUARK.U_Quark()
message = []    # your message as a list of bits
key = [] # your key as a list of bits
output = object.keyed_hash(message, key,output_type="hex")
# some code ....
```

### Test the Quark hash function

The implementation includes a testFile that tests the Quark hash functions with the values given in the official specification.


#### Sources 
[QUARK: A Lightweight Hash, Jean-Philippe Aumasson, NAGRA, route de Genève 22, 1033 Cheseaux, Switzerland](https://131002.net/quark/quark_full.pdf)

