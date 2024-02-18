#Find the weak key using matrix to reduce the complexity
from bitstring import BitArray
import numpy as np
from numpy.linalg import *
import time
start = time.time()

Bmatrix = np.array([[1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1],
                    [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
                    [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
                    [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]
                     ])


def row_echelon_form_binary(matrix):
    '''
    :return  m It is the row echelon form of matrix
    '''
    m = matrix.astype(int)  # Converting matrix data types to integer types (0 or 1)
    lead = 0

    for r in range(m.shape[0]):
        if lead >= m.shape[1]:
            break

        i = r
        while m[i, lead] == 0:
            i += 1
            if i == m.shape[0]:
                i = r
                lead += 1
                if m.shape[1] == lead:
                    return m

        m[[i, r]] = m[[r, i]]

        for i in range(m.shape[0]):
            if i != r and m[i, lead] == 1:
                m[i] ^= m[r]

        lead += 1

    return m
    
def circular_left_shift(bit_array, shift_amount):
    '''
    :bit_array Input bit array
    :shift_amount The number of bits for circular left shift 
    :return shifted_bits It is the bit_array after circular left shift shift_amount bits
    ''' 
    shifted_bits = bit_array[shift_amount:] + bit_array[:shift_amount]
    return shifted_bits

def generate_all_binary_strings(length):
    '''
    :length It is the length of bit array
    :return all_binary_strings All possible values of the bit arrays satisfying the length requirement
    '''
    all_binary_strings = []

    for i in range(2**length):
        # print(i)
        binary_string = format(i, f'0{length}b')
        all_binary_strings.append(BitArray(bin=binary_string))

    return all_binary_strings

def generateWeakkey(int_kq1,result_kq2_1,WeakKeyPair):
    '''
    :return WeakKeyPair The item in it is a pair of kq1 and kq2
    '''
    temp = []
    temp.append(int_kq1)
    vector0 = np.array([0])
    result_kq2_1 = np.append(result_kq2_1, vector0, axis=0)
    temp.append(result_kq2_1)
    WeakKeyPair.append(temp)

def PrintWeakkey(int_kq1,int_kq1_operated,M_np,WeakkeyArray):
    '''
    :int_kq1 In fact, it is kc1.
    :int_kq1_operated kc^(kc<<<5))
    :M_np It is the vector V mentioned in the essay
    :Weakkeyarray  It is used for stroring the the 4 kinds of weakkey 
    :return kc1 kc2
    '''
    
    int_M = M_np.astype(int)
    Matrix_constant = int_kq1_operated ^ int_M
    Matrix_constant = Matrix_constant.reshape(16,1)
    Expansion_Matrix = np.concatenate((Bmatrix,Matrix_constant), axis=1)     
    Expansion_RowSteppedMatrix = row_echelon_form_binary(Expansion_Matrix)
    rank = np.linalg.matrix_rank(Expansion_RowSteppedMatrix)
    if  rank == 15:   
        result_kq2_1 = solve(Expansion_RowSteppedMatrix[:15,:15],Expansion_RowSteppedMatrix[:15,-1:])%2  
        result_kq2_1 = result_kq2_1.reshape(15,).astype(int)
        generateWeakkey(int_kq1,result_kq2_1,WeakkeyArray)
        fileobj.write("Find!")
        fileobj.write("\n")
        fileobj.write("kc1:")       
        fileobj.write("\n")
        for j in range(len(int_kq1)):
            fileobj.write(str(int_kq1[j]))
        fileobj.write("\n")
        fileobj.write("kc2:")
        fileobj.write("\n")
        for j in range(len(result_kq2_1)):
            fileobj.write(str(result_kq2_1[j]))
        fileobj.write(str(0))
        fileobj.write("\n")

def expandWeakkey(WeakKeyPair):
    '''
    :return NewWeakKeyPair
     It expand the pair(kq1,kq2) to (kq1^1,kq2), (kq1,kq2^1),(kq1^1,Kq2^1),add all these pair into the original array 
    '''
    opposite = np.array([1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1])
    NewWeakKeyPair = WeakKeyPair
    for i in range(len(WeakKeyPair)):
        temp = []
        temp.append(WeakKeyPair[i][0] ^ opposite)
        temp.append(WeakKeyPair[i][1] ^ opposite)
        NewWeakKeyPair.append(temp)
        temp = []
        temp.append(WeakKeyPair[i][0])
        temp.append(WeakKeyPair[i][1] ^ opposite)
        NewWeakKeyPair.append(temp)
        temp = []
        temp.append(WeakKeyPair[i][0] ^ opposite)
        temp.append(WeakKeyPair[i][1] )
        NewWeakKeyPair.append(temp)
    return NewWeakKeyPair

def generateMainKey(kc1,kc2,kc3,kc4):
    K = []
    for i in range(16):
        K.append([])

    for i in range(16):
        if i % 4 == 0:
            K[i] = kc1[i//4*4:i//4*4+4]
        if i % 4 == 1:
            K[i] = kc2[i//4*4:i//4*4+4]        
        if i % 4 == 2:
            K[i] = kc3[i//4*4:i//4*4+4]
        if i % 4 == 3:
            K[i] = kc4[i//4*4:i//4*4+4]
    for i in range(16):
        if i == 0:
            MainKey = K[15-i]
            continue
        else:
            MainKey = np.concatenate((MainKey,K[15-i]), axis=0)
    MainKey = MainKey[::-1]
    temp = ''
    for i in range(len(MainKey)):
        temp = temp + str(MainKey[i])
    binary_data = BitArray(bin=temp)

    # 将二进制位数组转换为字节串（bytes）
    bytes_data = binary_data.tobytes()

    # 将字节串转换为十六进制表示
    hex_representation = bytes_data.hex().upper()

    print(temp)  
    print(hex_representation) 
 

bit_length = 15
all_binary_strings_kq1 = generate_all_binary_strings(bit_length)


WeakKeyPair1 = []
WeakKeyPair2 = []
WeakKeyPair3 = []
WeakKeyPair4 = []

zeroArray = BitArray(bin = '0')

for i in range(len(all_binary_strings_kq1)):
    print(i)
    kq1 = zeroArray*1 + all_binary_strings_kq1[i]
    temp = np.array(list(kq1.bin))
    int_kq1 = temp.astype(int)
    kq1_operated = kq1^(circular_left_shift(kq1,5))
    temp = np.array(list(kq1_operated.bin))
    int_kq1_operated = temp.astype(int)    
    if int_kq1_operated[0] == 0: 

        M_np = np.array([1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]) 
        
        for i in range(15):
            if int_kq1_operated[15 - i] == 1:
                M_np[1:15-i] = 1  # Set all elements in the M_np array before the corresponding position to 1.
                fileobj = open("WeakKey1229_Kq1AndKq2Is00_Kq1Is0_kq2Is1.txt", "a") 
                PrintWeakkey(int_kq1, int_kq1_operated, M_np,WeakKeyPair1)
                fileobj.close()
                break  # Jump out of the loop after finding a position that matches the conditions


        M_np = np.array([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]) 
        for i in range(15):
            if int_kq1_operated[15 - i] == 1:
                M_np[1:15-i] = 1  # Set all elements in the M_np array before the corresponding position to 1.
                fileobj = open("WeakKey1229_Kq1AndKq2Is10.txt", "a") 
                PrintWeakkey(int_kq1, int_kq1_operated, M_np,WeakKeyPair2)
                fileobj.close()
                break  # Jump out of the loop after finding a position that matches the conditions

        if int_kq1_operated[1] == 0:

            M_np = np.zeros(16)  # Initialise an all-zero array of length 16.

            for i in range(15):
                if int_kq1_operated[15 - i] == 1:
                    M_np[2:15-i] = 1  # Set all elements in the M_np array before the corresponding position to 1.
                    fileobj = open("WeakKey1229_Kq1AndKq2Is01.txt", "a") 
                    PrintWeakkey(int_kq1, int_kq1_operated, M_np,WeakKeyPair3)
                    fileobj.close()
                    break  # Jump out of the loop after finding a position that matches the conditions




            M_np = np.array([1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])  

            for i in range(15):
                if int_kq1_operated[15 - i] == 1:
                    M_np[2:15-i] = 1  #Set all elements in the M_np array before the corresponding position to 1.
                    fileobj = open("WeakKey1229_Kq1AndKq2Is11_Kq1Is00_kq2Is10.txt", "a")
                    PrintWeakkey(int_kq1, int_kq1_operated, M_np,WeakKeyPair4)
                    fileobj.close()
                    break  # Jump out of the loop after finding a position that matches the conditions

        elif int_kq1_operated[1] == 1:

            M_np = np.zeros(16)  # Initialise an all-zero array of length 16.

            for i in range(15):
                if int_kq1_operated[15 - i] == 1:
                    M_np[2:15-i] = 1  # Set all elements in the M_np array before the corresponding position to 1.
                    fileobj = open("WeakKey1229_Kq1AndKq2Is11_Kq1Is01_kq2Is01.txt", "a") 
                    PrintWeakkey(int_kq1, int_kq1_operated, M_np,WeakKeyPair4)
                    fileobj.close()
                    break  # Jump out of the loop after finding a position that matches the conditions


    elif int_kq1_operated[0] == 1:

        M_np = np.array([1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]) 
        
        for i in range(15):
            if int_kq1_operated[15 - i] == 1:
                M_np[1:15-i] = 1  # Set all elements in the M_np array before the corresponding position to 1.
                fileobj = open("WeakKey1229_Kq1AndKq2Is00_Kq1Is1_kq2Is0.txt", "a") 
                PrintWeakkey(int_kq1, int_kq1_operated, M_np,WeakKeyPair1)
                fileobj.close()
                break  # Jump out of the loop after finding a position that matches the conditions

        if int_kq1_operated[1]==0:

            M_np = np.array([1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])  

            for i in range(15):
                if int_kq1_operated[15 - i] == 1:
                    M_np[2:15-i] = 1  # Set all elements in the M_np array before the corresponding position to 1.
                    fileobj = open("WeakKey1229_Kq1AndKq2Is11_Kq1Is10_kq2Is00.txt", "a")
                    PrintWeakkey(int_kq1, int_kq1_operated, M_np,WeakKeyPair4)
                    fileobj.close()
                    break  # Jump out of the loop after finding a position that matches the conditions




NewWeakKeyPair1 = expandWeakkey(WeakKeyPair1)
NewWeakKeyPair2 = expandWeakkey(WeakKeyPair2)
NewWeakKeyPair3 = expandWeakkey(WeakKeyPair3)
NewWeakKeyPair4 = expandWeakkey(WeakKeyPair4)

# print(generateMainKey(NewWeakKeyPair[0][0],NewWeakKeyPair[0][1],NewWeakKeyPair[0][0],NewWeakKeyPair[0][1]))

MainKeyArr = []

indexnum = 4
for i in range(4):

    print("(1,1)")
    kc1 = NewWeakKeyPair1[i][0]
    kc2 = NewWeakKeyPair1[i][1]
    kc3 = NewWeakKeyPair1[i][0]
    kc4 = NewWeakKeyPair1[i][1]       
    generateMainKey(kc1,kc2,kc3,kc4)
    print("(1,2)")
    kc1 = NewWeakKeyPair1[i][0]
    kc2 = NewWeakKeyPair1[i][1]
    kc3 = NewWeakKeyPair2[i][0]
    kc4 = NewWeakKeyPair2[i][1]       
    generateMainKey(kc1,kc2,kc3,kc4)
    print("(1,3)")
    kc1 = NewWeakKeyPair1[i][0]
    kc2 = NewWeakKeyPair1[i][1]
    kc3 = NewWeakKeyPair3[i][0]
    kc4 = NewWeakKeyPair3[i][1]       
    generateMainKey(kc1,kc2,kc3,kc4)
    print("(1,4)")
    kc1 = NewWeakKeyPair1[i][0]
    kc2 = NewWeakKeyPair1[i][1]
    kc3 = NewWeakKeyPair4[i][0]
    kc4 = NewWeakKeyPair4[i][1]       
    generateMainKey(kc1,kc2,kc3,kc4)

    print("(2,1)")
    kc1 = NewWeakKeyPair2[i][0]
    kc2 = NewWeakKeyPair2[i][1]
    kc3 = NewWeakKeyPair1[i][0]
    kc4 = NewWeakKeyPair1[i][1]       
    generateMainKey(kc1,kc2,kc3,kc4)
    print("(2,2)")
    kc1 = NewWeakKeyPair2[i][0]
    kc2 = NewWeakKeyPair2[i][1]
    kc3 = NewWeakKeyPair2[i][0]
    kc4 = NewWeakKeyPair2[i][1]       
    generateMainKey(kc1,kc2,kc3,kc4)
    print("(2,3)")
    kc1 = NewWeakKeyPair2[i][0]
    kc2 = NewWeakKeyPair2[i][1]
    kc3 = NewWeakKeyPair3[i][0]
    kc4 = NewWeakKeyPair3[i][1]       
    generateMainKey(kc1,kc2,kc3,kc4)
    print("(2,4)")
    kc1 = NewWeakKeyPair2[i][0]
    kc2 = NewWeakKeyPair2[i][1]
    kc3 = NewWeakKeyPair4[i][0]
    kc4 = NewWeakKeyPair4[i][1]       
    generateMainKey(kc1,kc2,kc3,kc4)

    print("(3,1)")
    kc1 = NewWeakKeyPair3[i][0]
    kc2 = NewWeakKeyPair3[i][1]
    kc3 = NewWeakKeyPair1[i][0]
    kc4 = NewWeakKeyPair1[i][1]       
    generateMainKey(kc1,kc2,kc3,kc4)
    print("(3,2)")
    kc1 = NewWeakKeyPair3[i][0]
    kc2 = NewWeakKeyPair3[i][1]
    kc3 = NewWeakKeyPair2[i][0]
    kc4 = NewWeakKeyPair2[i][1]       
    generateMainKey(kc1,kc2,kc3,kc4)
    print("(3,3)")
    kc1 = NewWeakKeyPair3[i][0]
    kc2 = NewWeakKeyPair3[i][1]
    kc3 = NewWeakKeyPair3[i][0]
    kc4 = NewWeakKeyPair3[i][1]       
    generateMainKey(kc1,kc2,kc3,kc4)
    print("(3,4)")
    kc1 = NewWeakKeyPair3[i][0]
    kc2 = NewWeakKeyPair3[i][1]
    kc3 = NewWeakKeyPair4[i][0]
    kc4 = NewWeakKeyPair4[i][1]       
    generateMainKey(kc1,kc2,kc3,kc4)

    print("(4,1)")
    kc1 = NewWeakKeyPair4[i][0]
    kc2 = NewWeakKeyPair4[i][1]
    kc3 = NewWeakKeyPair1[i][0]
    kc4 = NewWeakKeyPair1[i][1]       
    generateMainKey(kc1,kc2,kc3,kc4)
    print("(4,2)")
    kc1 = NewWeakKeyPair4[i][0]
    kc2 = NewWeakKeyPair4[i][1]
    kc3 = NewWeakKeyPair2[i][0]
    kc4 = NewWeakKeyPair2[i][1]       
    generateMainKey(kc1,kc2,kc3,kc4)
    print("(4,3)")
    kc1 = NewWeakKeyPair4[i][0]
    kc2 = NewWeakKeyPair4[i][1]
    kc3 = NewWeakKeyPair3[i][0]
    kc4 = NewWeakKeyPair3[i][1]       
    generateMainKey(kc1,kc2,kc3,kc4)
    print("(4,4)")
    kc1 = NewWeakKeyPair4[i][0]
    kc2 = NewWeakKeyPair4[i][1]
    kc3 = NewWeakKeyPair4[i][0]
    kc4 = NewWeakKeyPair4[i][1]       
    generateMainKey(kc1,kc2,kc3,kc4)
    
end = time.time()

print (str(end-start))



