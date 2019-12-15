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
    print("________________Test du S-Quark :___________________")
    print("Expected digest : ",expected_output)
    print("S-Quark output (digest) : ",output)
    if output == expected_output :
        print("Correct")
    else :
        print("Wrong")
    print("____________________ End of test ___________________")


"""_____________ Main Code ____________"""

test_U_Quark() # test the U-QUARK
test_S_Quark() # test the S-QUARK
test_D_Quark() # test the D-QUARK
#object = QUARK.U_Quark()
#output = object.keyed_hash([0,0,1,1,1,0,0,0],[],output_type="hex")
#print("U-Quark output (digest) : ",output)
