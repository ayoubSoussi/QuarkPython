import numpy as np
from bitstring import BitArray
import math
import sys

# Cette version python du Quark va servir a la validation de l'implementation en VHDL :
# En generant des (message, valeur hashe) et utilisant ces valeurs dans le testbench
# pour comparer avec l'implementation VHDL

class Quark :
    """ Given a message m and a key k(lists of bits),
    Quark class outputs the hashed value of the
    message using Quark family hash functions """
    r=None #rate
    c=None #capacity
    n=None #output lenght
    b=None #size of the state

    state=None #internal state
    def __init__(self) :
        self.message_nb = None       # number of message blocks
        self.output_nb = None       # number of output blocks
    def keyed_hash(self,m,k,output_type="bits") :
        """ Given a message m and a key k, hash function returns the hashed
               value of th message using the key k in one of the instances of the
                      Quark functions family  """
        m = np.array(m).astype(int) # message
        k = np.array(k).astype(int) # key
        keyed_message = np.append(k,m) # key+message
        if output_type == "hex" :
            return self.bitsToHex(self.hash(keyed_message)) # output is in hex format
        return self.hash(keyed_message) # output is in bits array format
    def hash(self,m) :
        """ Given a message m, hash function return the hashed
               value of th message using one of the instances of the
                      Quark functions family  """
        self.m = np.array(m).astype(int) # message
        self.initialize() # initialization phase
        self.absorb() # absorption phase
        result = self.squeeze() # squeezing phase
        return result
    def initialize(self) :
        """Initialization phase of Quark function"""
        self.m = np.append(self.m,np.array([1]))    # append '1' to the message
        while (len(self.m)%self.r != 0) :           # while message's lenght is not multiple of the rate
            self.m = np.append(self.m,np.array([0]))# append a '0' to the message
        #print("the message after appending : ", self.m)
        self.message_nb = len(self.m)//self.r                # number of message r_bits blocks
        #print("the number of message blocks : ",self.message_nb)
        self.m = np.split(self.m,self.message_nb)           # split the message to blocks of 'r' bits each
    def absorb(self) :
        self.a = False
        for i in range(0,self.message_nb) :
            m_block = self.m[i] # message block of r bits
            #print("the message block : ", m_block)
            state_block = self.state[self.b-self.r:] # last r bits of the state
            state_block = np.bitwise_xor(m_block,state_block) # state XOR message
            self.state[self.b-self.r:] = state_block # update the internal state
            #print("state after first XOR : ",self.bitsToHex(self.state))
            self.state = self.permute(self.state) # permute the internal state
            #print("state after absorption iteration: ",self.bitsToHex(self.state))
        #print("state after absorption : ",self.bitsToHex(self.state))
    def squeeze(self) :
        self.a = True
        self.output_nb = self.n//self.r  # number of blocks of the output
        result = np.empty((self.output_nb,self.r),np.int8) # create the output arrays
        result[0] = self.state[self.b-self.r:]   # add the last r bits block of the state
        for i in range(1,self.output_nb) :
            self.state = self.permute(self.state)  # permute the internal state
            #print("squeeze step ",i," :",self.bitsToHex(self.state))
            result[i] = self.state[self.b-self.r:]   # add the last r bits block of the state
        result = np.concatenate((result),axis=None)  # concatenate the digest blocks into one array
        return result
    def permute(self,state) :
        """Given a state as an array of b bits, the permutation
        function update it and return a new state of b bits too"""
        # initialization phase
        Xt = state[0:self.b//2] # initialize NFSR of b/2 bits
        Yt = state[self.b//2:] # initialize NFSR of b/2 bits
        Lt = np.ones(int(math.ceil(math.log(4*self.b,2)))).astype(int) # initialize LFSR of [log 4b] bits
        #print(math.ceil(math.log(4*self.b,2)))
        #print(-1," => X : ", self.bitsToHex(Xt), " Y : ", self.bitsToHex(Yt), " L : ", self.bitsToHex(Lt))
        # update phase
        for i in range(4*self.b) :   # update 4b times

            ht = self.h(Xt, Yt, Lt) # calculate ht
            #print(" le H est :", ht, "le P : ",self.p(Lt),"le G : ",self.g(Yt), "le f :", self.f(Xt))
            Xt = np.append(Xt[1:],np.array([Yt[0] ^ self.f(Xt) ^ ht])) # update Xt
            Yt = np.append(Yt[1:],np.array([self.g(Yt) ^ ht])) # update Yt
            Lt = np.append(Lt[1:],np.array([self.p(Lt)])) # update Lt
            #if self.a == True :
            #print(i," => X : ", self.bitsToHex(Xt), " Y : ", self.bitsToHex(Yt), " L : ", Lt)
        new_state = np.append(Xt,Yt) # calculate the output state : (X(4b)......Y(4b))
        return new_state # return the new internal state

    def p(self,L) :
        return L[0] ^ L[3] # return L[0] xor L[3]

    def hexToBits(self,hex_string) :
        """"Convert a hexadecimal representation
        of a number to an array of bits"""
        res = BitArray(hex=hex_string) # convert the string to bitArray
        res = np.array(list(res.bin)).astype(np.int) # convert the bitArray to a numpy array of bits
        return res
    def bitsToHex(self,bitsArray) :
        """ Convert an array of bits to an hexadecimal
        representation """
        bitsString = np.array2string(bitsArray, max_line_width=len(bitsArray)+2, separator='')[1:-1] # bits representation of the array
        print(sys.version[0])
        if (sys.version[0] == '2') :
            ####### Python2
            hex_representation = hex(int(bitsString, 2))[2:-1] #  string hexadecimal representation
        elif (sys.version[0] == '3') :
            ####### Python3
            hex_representation = hex(int(bitsString, 2))[2:] #  string hexadecimal representation


        hex_caracters_nb = len(bitsArray)//4 ; # the lenght of the string needed
        hex_representation = "0"*(hex_caracters_nb-len(hex_representation)) + hex_representation
        return hex_representation.upper() # return the hex representation in upper case

"""___________U-QUARK___________"""
class U_Quark(Quark) :
    """ Given a message m and a key k,
    Quark class outputs the hashed value
    of the message using U-Quark """
    def __init__(self):
        Quark.__init__(self)
        # initialize U-Quark parameters
        self.r = 8
        self.c = 128
        self.n = 136
        self.b = self.r + self.c

        # initialize the internal state
        self.state = self.hexToBits("D8DACA44414A099719C80AA3AF065644DB")
    def f(self,X) :
        resultat = X[0] ^ X[9] ^ X[14] ^ X[21] ^ X[28] ^ X[33] ^ X[37] ^ X[45] ^ X[50] ^ X[52] ^ X[55]
        resultat = resultat ^ (X[55]&X[59]) ^ (X[33]&X[37]) ^ (X[9]&X[15])
        resultat = resultat ^ (X[45]&X[52]&X[55]) ^ (X[21]&X[28]&X[33])
        resultat = resultat ^ (X[9]&X[28]&X[45]&X[59]) ^ (X[33]&X[37]&X[52]&X[55]) ^ (X[15]&X[21]&X[55]&X[59])
        resultat = resultat ^ (X[37]&X[45]&X[52]&X[55]&X[59]) ^ (X[9]&X[15]&X[21]&X[28]&X[33]) ^ (X[21]&X[28]&X[33]&X[37]&X[45]&X[52])
        return resultat
    def g(self,Y) :
        resultat = Y[0] ^ Y[7] ^ Y[16] ^ Y[20] ^ Y[30] ^ Y[35] ^ Y[37] ^ Y[42] ^ Y[49] ^ Y[51] ^ Y[54]
        resultat = resultat ^ (Y[54]&Y[58]) ^ (Y[35]&Y[37]) ^ (Y[7]&Y[15])
        resultat = resultat ^ (Y[42]&Y[51]&Y[54]) ^ (Y[20]&Y[30]&Y[35])
        resultat = resultat ^ (Y[7]&Y[30]&Y[42]&Y[58]) ^ (Y[35]&Y[37]&Y[51]&Y[54]) ^ (Y[15]&Y[20]&Y[54]&Y[58])
        resultat = resultat ^ (Y[37]&Y[42]&Y[51]&Y[54]&Y[58]) ^ (Y[7]&Y[15]&Y[20]&Y[30]&Y[35]) ^ (Y[20]&Y[30]&Y[35]&Y[37]&Y[42]&Y[51])
        return resultat
    def h(self,X,Y,L) :
        resultat = L[0] ^ X[1] ^ Y[2] ^ X[4] ^ Y[10] ^ X[25] ^ X[31] ^ Y[43] ^ X[56] ^ Y[59]
        resultat = resultat ^ (Y[3]&X[55]) ^ (X[46]&X[55]) ^ (X[55]&Y[59])
        resultat = resultat ^ (Y[3]&X[25]&X[46]) ^ (Y[3]&X[46]&X[55]) ^ (Y[3]&X[46]&Y[59])
        resultat = resultat ^ (L[0]&X[25]&X[46]&Y[59]) ^ (L[0]&X[25])
        return resultat

"""___________D-QUARK___________"""

class D_Quark(Quark) :
    """ Given a message m and a key k,
    Quark class outputs the hashed value
    of the message using D-Quark """
    def __init__(self):
        Quark.__init__(self)
        # initialize U-Quark parameters
        self.r = 16
        self.c = 160
        self.n = 176
        self.b = self.r + self.c

        # initialize the internal state
        self.state = self.hexToBits("CC6C4AB7D11FA9BDF6EEDE03D87B68F91BAA706C20E9")
    def f(self,X) :
        resultat = X[0] ^ X[11] ^ X[18] ^ X[27] ^ X[36] ^ X[42] ^ X[47] ^ X[58] ^ X[64] ^ X[67] ^ X[71]
        resultat = resultat ^ (X[71]&X[79]) ^ (X[42]&X[47]) ^ (X[11]&X[19])
        resultat = resultat ^ (X[58]&X[67]&X[71]) ^ (X[27]&X[36]&X[42])
        resultat = resultat ^ (X[11]&X[36]&X[58]&X[79]) ^ (X[42]&X[47]&X[67]&X[71]) ^ (X[19]&X[27]&X[71]&X[79])
        resultat = resultat ^ (X[47]&X[58]&X[67]&X[71]&X[79]) ^ (X[11]&X[19]&X[27]&X[36]&X[42]) ^ (X[27]&X[36]&X[42]&X[47]&X[58]&X[67])
        return resultat
    def g(self,Y) :
        resultat = Y[0] ^ Y[9] ^ Y[20] ^ Y[25] ^ Y[38] ^ Y[44] ^ Y[47] ^ Y[54] ^ Y[63] ^ Y[67] ^ Y[69]
        resultat = resultat ^ (Y[69]&Y[78]) ^ (Y[44]&Y[47]) ^ (Y[9]&Y[19])
        resultat = resultat ^ (Y[54]&Y[67]&Y[69]) ^ (Y[25]&Y[38]&Y[44])
        resultat = resultat ^ (Y[9]&Y[38]&Y[54]&Y[78]) ^ (Y[44]&Y[47]&Y[67]&Y[69]) ^ (Y[19]&Y[25]&Y[69]&Y[78])
        resultat = resultat ^ (Y[47]&Y[54]&Y[67]&Y[69]&Y[78]) ^ (Y[9]&Y[19]&Y[25]&Y[38]&Y[44]) ^ (Y[25]&Y[38]&Y[44]&Y[47]&Y[54]&Y[67])
        return resultat
    def h(self,X,Y,L) :
        resultat = L[0] ^ X[1] ^ Y[2] ^ X[5] ^ Y[12] ^ Y[24] ^ X[35] ^ X[40] ^ X[48] ^ Y[55] ^ Y[61] ^ X[72] ^ Y[79]
        resultat = resultat ^ (Y[4]&X[68]) ^ (X[57]&X[68]) ^ (X[68]&Y[79])
        resultat = resultat ^ (Y[4]&X[35]&X[57]) ^ (Y[4]&X[57]&X[68]) ^ (Y[4]&X[57]&Y[79])
        resultat = resultat ^ (L[0]&X[35]&X[57]&Y[79]) ^ (L[0]&X[35])
        return resultat

"""___________S-QUARK___________"""
class S_Quark(Quark) :
    """ Given a message m and a key k,
    Quark class outputs the hashed value
    of the message using S-Quark """
    def __init__(self):
        Quark.__init__(self)
        # initialize U-Quark parameters
        self.r = 32
        self.c = 224
        self.n = 256
        self.b = self.r + self.c

        # initialize the internal state
        self.state = self.hexToBits("397251CEE1DE8AA73EA26250C6D7BE128CD3E79DD718C24B8A19D09C2492DA5D")
    def f(self,X) :
        resultat = X[0] ^ X[16] ^ X[26] ^ X[39] ^ X[52] ^ X[61] ^ X[69] ^ X[84] ^ X[94] ^ X[97] ^ X[103]
        resultat = resultat ^ (X[103]&X[111]) ^ (X[61]&X[69]) ^ (X[16]&X[28])
        resultat = resultat ^ (X[84]&X[97]&X[103]) ^ (X[39]&X[52]&X[61])
        resultat = resultat ^ (X[16]&X[52]&X[84]&X[111]) ^ (X[61]&X[69]&X[97]&X[103]) ^ (X[28]&X[39]&X[103]&X[111])
        resultat = resultat ^ (X[69]&X[84]&X[97]&X[103]&X[111]) ^ (X[16]&X[28]&X[39]&X[52]&X[61]) ^ (X[39]&X[52]&X[61]&X[69]&X[84]&X[97])
        return resultat
    def g(self,Y) :
        resultat = Y[0] ^ Y[13] ^ Y[30] ^ Y[37] ^ Y[56] ^ Y[65] ^ Y[69] ^ Y[79] ^ Y[92] ^ Y[96] ^ Y[101]
        resultat = resultat ^ (Y[101]&Y[109]) ^ (Y[65]&Y[69]) ^ (Y[13]&Y[28])
        resultat = resultat ^ (Y[79]&Y[96]&Y[101]) ^ (Y[37]&Y[56]&Y[65])
        resultat = resultat ^ (Y[13]&Y[56]&Y[79]&Y[109]) ^ (Y[65]&Y[69]&Y[96]&Y[101]) ^ (Y[28]&Y[37]&Y[101]&Y[109])
        resultat = resultat ^ (Y[69]&Y[79]&Y[96]&Y[101]&Y[109]) ^ (Y[13]&Y[28]&Y[37]&Y[56]&Y[65]) ^ (Y[37]&Y[56]&Y[65]&Y[69]&Y[79]&Y[96])
        return resultat
    def h(self,X,Y,L) :
        resultat = L[0] ^ X[1] ^ Y[3] ^ X[7] ^ Y[18] ^ Y[34] ^ X[47] ^ X[58] ^ Y[71] ^ Y[80] ^ X[90] ^ Y[91] ^ X[105] ^ Y[111]
        resultat = resultat ^ (Y[8]&X[100]) ^ (X[72]&X[100]) ^ (X[100]&Y[111])
        resultat = resultat ^ (Y[8]&X[47]&X[72]) ^ (Y[8]&X[72]&X[100]) ^ (Y[8]&X[72]&Y[111])
        resultat = resultat ^ (L[0]&X[47]&X[72]&Y[111]) ^ (L[0]&X[47])
        return resultat
