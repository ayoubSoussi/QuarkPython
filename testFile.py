import QUARK


def test_U_Quark() :
    '''Test U-Quark using an empty message'''
    expected_output = "126B75BCAB23144750D08BA313BBD800A4" # expected digest
    object = QUARK.U_Quark()
    output = object.keyed_hash([],[],output_type="hex")
    print("___________________Test du U-Quark :___________________")
    print("Expected digest : ",expected_output)
    print("U-Quark output (digest) : ",output)
    if output == expected_output :
        print("Correct")
    else :
        print("Wrong")
    print("____________________ End of test ___________________")

def test_D_Quark() :
    '''Test D-Quark using an empty message'''
    expected_output = "82C7F380E231578E2FF4C2A402E18BF37AEA8477298D" # expected digest
    object = QUARK.D_Quark()
    output = object.keyed_hash([],[],output_type="hex")
    print("_____________________Test du D-Quark :____________________")
    print("Expected digest : ",expected_output)
    print("D-Quark output (digest) : ",output)
    if output == expected_output :
        print("Correct")
    else :
        print("Wrong")
    print("____________________ End of test ___________________")

def test_S_Quark() :
    '''Test S-Quark using an empty message'''
    expected_output = "03256214B92E811C321AE86BAB4B0E7AE9C22C42882FCCDE8C22BFF6A0A1D6F1" # expected digest
    object = QUARK.S_Quark()
    output = object.keyed_hash([],[],output_type="hex")
    print("_____________________Test du S-Quark :____________________")
    print("Expected digest : ",expected_output)
    print("S-Quark output (digest) : ",output)
    if output == expected_output :
        print("Correct")
    else :
        print("Wrong")
    print("____________________ End of test ___________________")
def test_Quark() :
    '''Test S-Quark using an empty message'''
    object = QUARK.U_Quark()
    message1 = object.hexToBits("6D7BE128CD3E79DDA73EA26250CCEE1DE8AA73EA240AC24B8A19D09C2492DA5D")
    key1     = object.hexToBits("20CA51CEE1DE8AA73EA2402BC6D7BE128CD3E79DD718C24B8A19D094590CAD21")

    message2 = 256*['0']
    key2     = 256*['0']

    message3 = 256*['1']
    key3 = 256*['0']
    message4 = object.hexToBits("EA26250CCEE1DE8AA733EA2625CA5CEE1DE73EA29D79DDA73EA26250CCEE1DE2")
    key4     = object.hexToBits("250C6D7BE128CD3E79DDEA26250C6D7BE128CD3E79DD718C24B8A19D09C2492D")
    message5 = object.hexToBits("3E79DD718C24B8A150C397251CEE1DE8AA73EA2D718C24B8A19D09C24CA32789")
    key5     = object.hexToBits("D09C2492DA5DDE8AA73EA26250C6D7BE128CD3E79DD718C24B8A19D09C2492DA")

    object = QUARK.U_Quark()
    output = object.keyed_hash(message1,key1,output_type="hex")
    print("S-Quark output (digest) : ",output)

    object = QUARK.D_Quark()
    #output = object.keyed_hash(message2,key2,output_type="hex")
    print("S-Quark output (digest) : ",output)

    object = QUARK.D_Quark()
    #output = object.keyed_hash(message3,key3,output_type="hex")
    print("S-Quark output (digest) : ",output)

    object = QUARK.D_Quark()
    #output = object.keyed_hash(message4,key4,output_type="hex")
    print("S-Quark output (digest) : ",output)

    object = QUARK.D_Quark()
    #output = object.keyed_hash(message5,key5,output_type="hex")
    print("S-Quark output (digest) : ",output)
    print("________________Test du S-Quark :___________________")
    #print("Expected digest : ",expected_output)
    print("S-Quark output (digest) : ",output)
    if output == expected_output :
        print("Correct")
    else :
        print("Wrong")
    print("____________________ End of test ___________________")


"""_____________ Main Code ____________"""

#test_U_Quark() # test the U-QUARK
test_S_Quark() # test the S-QUARK
#test_D_Quark() # test the D-QUARK
#object = QUARK.U_Quark()
#output = object.keyed_hash([0,0,1,1,1,0,0,0],[],output_type="hex")
#print("U-Quark output (digest) : ",output)
