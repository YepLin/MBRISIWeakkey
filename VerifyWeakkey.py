from unittest import case

from bitstring import BitArray

from collections import Counter



def circular_left_shift(bit_array, shift_amount):
    '''
    :bit_array Input bit array
    :shift_amount The number of bits for circular left shift 
    :return shifted_bits It is the bit_array after circular left shift shift_amount bits
    ''' 
    shifted_bits = bit_array[shift_amount:] + bit_array[:shift_amount]
    return shifted_bits


def operate(K, L0, R0):
    """
    :param K: the key for this round
    :param LR0: the left branch
    :param LR1: the right branch
    :return: the result after encryption
    """

    L0_left_shift_1 = circular_left_shift(L0, 1)
    L0_left_shift_8 = circular_left_shift(L0, 8)
    L0_left_shift_2 = circular_left_shift(L0, 2)
    # print(L0, R0, L0_left_shift_1)
    L0_result = (L0_left_shift_1 ^ L0_left_shift_8) ^ R0 ^ L0_left_shift_2
    addition_mod_int = (int(L0_result.bin, 2) + int(K.bin, 2)) % 65536
    # if addition_mod_int == 65536:
    #     addition_mod_int = 0
    # print(addition_mod_int)
    addition_mod = BitArray(bin=bin(addition_mod_int)[2:].zfill(16))
    # print(addition_mod)
    return addition_mod


def decryption_operate(K, L0, R0):
    """
    :param K: the key for this round
    :param LR0: the left branch
    :param LR1: the right branch
    :return: the result after encryption
    """
    L0_left_shift_1 = circular_left_shift(L0, 1)
    L0_left_shift_8 = circular_left_shift(L0, 8)
    L0_left_shift_2 = circular_left_shift(L0, 2)
    # 减模运算
    subtraction_mod_int = int(R0.bin, 2) - int(K.bin, 2)
    if subtraction_mod_int < 0:
        subtraction_mod_int = 65536 + subtraction_mod_int
        # if subtraction_mod_int == 65536:
        #     subtraction_mod_int = 0
    subtraction_mod = BitArray(bin=bin(subtraction_mod_int)[2:].zfill(16))
    R0_result = subtraction_mod ^ L0_left_shift_2 ^ (L0_left_shift_1 ^ L0_left_shift_8)
    return R0_result

def encryption(plaintext, K,round):
    """
    :param plaintext: one-dimensional bit array,
    :param k:  Key, two-dimensional bit array
    :param n: Encryption rounds
    :return: returning ciphertext.

    """

    L0 = plaintext[:16]
    R0 = plaintext[16:32]
    for i in range(round):
        L0_result = operate(K[i], L0, R0)
        R0_result = L0
        L0 = L0_result
        R0 = R0_result
        # if i == 8:
        #     print("加密第9轮的结果为：",L0.bin,R0.bin)
    # print(L0+R0)
    return L0 + R0

def decryption(ciphertext, K):
    L0 = ciphertext[0:16]
    R0 = ciphertext[16:32]
    for i in range(9, -1, -1):
        L0_result = R0
        R0_result = decryption_operate(K[i], L0_result, L0)
        L0 = L0_result
        R0 = R0_result
        # if i == 9:
        #     print("解密第一轮的结果为：",L0.bin,R0.bin)
    return L0 + R0

def generate_all_binary_strings(length):
    '''
    :length It is the length of bit array
    :return all_binary_strings All possible values of the bit arrays satisfying the length requirement
    '''
    all_binary_strings = []

    for i in range(2**length):
        print(i)
        binary_string = format(i, f'0{length}b')
        all_binary_strings.append(BitArray(bin=binary_string))

    return all_binary_strings


def expansion_key(initial_key):
    key_list = []
    kc1 = initial_key[3::-1] + initial_key[19:15:-1] + initial_key[35:31:-1] + initial_key[51:47:-1]
    kc2 = initial_key[7:3:-1] + initial_key[23:19:-1] + initial_key[39:35:-1] + initial_key[55:51:-1]
    kc3 = initial_key[11:7:-1] + initial_key[27:23:-1] + initial_key[43:39:-1] + initial_key[59:55:-1]
    kc4 = initial_key[15:11:-1] + initial_key[31:27:-1] + initial_key[47:43:-1] + initial_key[63:59:-1]

    ks1 = circular_left_shift(kc1, 5)
    ks2 = circular_left_shift(kc2, 3)
    ks3 = circular_left_shift(kc3, 5)
    ks4 = circular_left_shift(kc4, 3)
    kq1 = kc1 ^ ks1
    kq2 = kc2 ^ ks2
    kq3 = kc3 ^ ks3
    kq4 = kc4 ^ ks4

    kq1_int = int(kq1.bin, 2)
    kq2_int = int(kq2.bin, 2)
    kq3_int = int(kq3.bin, 2)
    kq4_int = int(kq4.bin, 2)
    sk1_int = (kq1_int + kq2_int) % 65536
    sk2_int = (kq3_int + kq4_int) % 65536
    sk1 = BitArray(bin=bin(sk1_int)[2:].zfill(16))
    sk2 = BitArray(bin=bin(sk2_int)[2:].zfill(16))

    key_list.append(sk1)
    key_list.append(sk2)
    for i in range(2, 10):
        sk_i_int = (int(key_list[i - 1].bin, 2) + int(key_list[i - 2].bin, 2)) % 65536
        sk_i = BitArray(bin=bin(sk_i_int)[2:].zfill(16))
        key_list.append(sk_i)

    return key_list


#Verify that the differential probability is 1 under the master key in variable k
k = BitArray(bin='0000100100001001000010100000101000000010000000100110011101100111')
key_list = expansion_key(k)

bit_length = 16
all_binary_strings_right = generate_all_binary_strings(bit_length)

num = 0
p = []
output_counts = Counter()
for i in range(len(all_binary_strings_right)):
    print(i)
    index = 16
    zeroArray = BitArray(bin = '0')
    plaintext0 = zeroArray*index + all_binary_strings_right[i] + zeroArray*(16- index)
    delta = BitArray(bin='00000000100000110000000000001010') 
    plaintext1 = plaintext0 ^ delta
    ciphertext0 = encryption(plaintext0, key_list,4)
    ciphertext1 = encryption(plaintext1, key_list,4)
    belta = ciphertext0 ^ ciphertext1
    belta_int = int(belta.bin,2)
    output_counts[belta_int] += 1



fileobj = open("result.txt", "w")

# Print out the value and the number of times it occurs
for output, count in output_counts.items():
    temp = output
    temp_bin = BitArray(bin=bin(temp)[2:].zfill(32))
    fileobj.write(f"Ouput: {temp_bin.bin} Number of occurrences: {count}\n")

fileobj.close()
print(len(output_counts))

