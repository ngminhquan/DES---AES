#input
from decimal import DecimalException
from re import T


pt = "02468ACEECA86420"
key = "0F1571C947D9E859"

#transform hexadecimal to binary
def hex_to_bin(s):
    trans = {
        "0": "0000",
        "1": "0001",
        "2": "0010",
        "3": "0011",
        "4": "0100",
        "5": "0101",
        "6": "0110",
        "7": "0111",
        "8": "1000",
        "9": "1001",
        "A": "1010",
        "B": "1011",
        "C": "1100",
        "D": "1101",
        "E": "1110",
        "F": "1111"}
    bin = ""
    for i in range(len(s)):
        bin = bin + trans[s[i]]
    return bin

#print(hex_to_bin(pt))

#transform binary to hexadecimal
def bin_to_hex(s):
    trans = {
        "0000": "0",
        "0001": "1",
        "0010": "2",
        "0011": "3",
        "0100": "4",
        "0101": "5",
        "0110": "6",
        "0111": "7",
        "1000": "8",
        "1001": "9",
        "1010": "A",
        "1011": "B",
        "1100": "C",
        "1101": "D",
        "1110": "E",
        "1111": "F"}
    hex = ""
    for i in range(0, len(s), 4):
        ch = ""
        ch += s[i]
        ch += s[i+1]
        ch += s[i+2]
        ch += s[i+3]
        hex = hex + trans[ch]
    return hex
#print(bin_to_hex())

#initial permutation table
IP = [58, 50, 42, 34, 26, 18, 10, 2,
      60, 52, 44, 36, 28, 20, 12, 4,
      62, 54, 46, 38, 30, 22, 14, 6,
      64, 56, 48, 40, 32, 24, 16, 8,
      57, 49, 41, 33, 25, 17, 9, 1,
      59, 51, 43, 35, 27, 19, 11, 3,
      61, 53, 45, 37, 29, 21, 13, 5,
      63, 55, 47, 39, 31, 23, 15, 7]

#inverse initial permutation
InvIP = [40, 8, 48, 16, 56, 24, 64, 32,
         39, 7, 47, 15, 55, 23, 63, 31,
         38, 6, 46, 14, 54, 22, 62, 30,
         37, 5, 45, 13, 53, 21, 61, 29,
         36, 4, 44, 12, 52, 20, 60, 28,
         35, 3, 43, 11, 51, 19, 59, 27,
         34, 2, 42, 10, 50, 18, 58, 26,
         33, 1, 41, 9, 49, 17, 57, 25]

#permutation through IP
def permute(k, arr, n):
    permutation = ""
    for i in range(0, n):
        permutation = permutation + k[arr[i] - 1]
    return permutation
#print(permute(hex_to_bin(pt), IP, 64))

#Expansion permutation
EP = [32, 1, 2, 3, 4, 5,
      4, 5, 6, 7, 8, 9,
      8, 9, 10, 11, 12, 13,
      12, 13, 14, 15, 16, 17,
      16, 17, 18, 19, 20, 21,
      20, 21, 22, 23, 24, 25,
      24, 25, 26, 27, 28, 29,
      28, 29, 30, 31, 32, 1]

#Expansion 32 bits to 48 bits
def ep32_48(k, arr, n):
    ep = ""
    for i in range (0, n):
        ep = ep +k[arr[i]-1]
    return ep

#XOR pt_48bits with key_48bits
def xor(a, b):
    c = ""
    for i in range(len(a)):
        if a[i] == b[i]:
            c += "0"
        else: c += "1"
    return c

#Transform decimal to binary
def dec_to_bin(s):
        bin = ""
        while (s != 0):
            r = s % 2
            bin += str(r)
            s //= 2
        return bin
#print(dec_to_bin(3))

#Transform binary to decimal
def bin_to_dec(s):
    dec, i = 0, 0
    while (s != 0):
        r = s % 10
        dec += r * pow(2,i)
        s //= 10
        i += 1
    return dec
#(bin_to_dec(1010))

#S_box: 48bits to 32bits
S_box = [[[14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
          [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5 , 3, 8],
          [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],       #S1
          [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]],

          [[15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
          [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
          [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],       #S2
          [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9]],

          [[10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
           [13, 7, 0, 9, 3, 4, 6, 10, 2 , 8, 5, 14, 12, 11, 15, 1],
           [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],      #S3
           [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12]],
           
          [[7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5 , 11, 12, 4, 15],
           [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
           [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],     #S4
           [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14]],
            
          [[2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
           [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
           [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],       #S5
           [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3]],

          [[12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
           [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
           [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],       #S6
           [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13]],
              
          [[4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
           [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
           [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],      #S7
           [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12]],
               
          [[13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
           [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
           [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],     #S8
           [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]]]


#P_box
P_box = [16, 7, 20, 21, 29, 12, 28, 17,
         1, 15, 23, 26, 5, 18, 31, 10,
         2, 8, 24, 14, 32, 27, 3, 9,
         19, 13, 30, 6, 22, 11, 4, 25]

#Key generation
#Permute Choice 1
PC1 = [57, 49, 41, 33, 25, 17, 9,
       1, 58, 50, 42, 34, 26, 18,
       10, 2, 59, 51, 43, 35, 27,
       19, 11, 3, 60, 52, 44, 36,
       63, 55, 47, 39, 31, 23, 15,
       7, 62, 54, 46, 38, 30, 22,
       14, 6, 61, 53, 45, 37, 29,
       31, 13, 5, 28, 20, 12, 4]

#Permute Choice 2
PC2 = [14, 17, 11, 24, 1, 5, 3, 28,
       15, 6, 21, 10, 23, 19, 12, 4,
       26, 8, 16, 7, 27, 20, 13, 2,
       41, 52, 31, 37, 47, 55, 30, 40,
       51, 45, 33, 48, 44, 49, 39, 56,
       34, 53, 46, 42, 50, 36, 29, 32]

#Left Shift Table
LSTable = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]

#Left Shift n bit
def left_shift(s, shift, n):
    A = ""
    
    for j in range (shift,n):
        A += s[j]
    for i in range(shift):
        k = s[i]
        A += k
    return A
#print(left_shift("12345", 2, 5))



def key_generation(C):
    key = permute(key, PC1, 56)         #ignore every eighth bit and permute
    C = key[0:28]                       #56bits key => two 28bits
    D = key[28:56]
    rkb = []
    rk = []
    for i in range(0, 16):
        C = left_shift(C, LSTable[i], 28)
        D = left_shift(D, LSTable[i], 28)
        combine = C + D
        round_key = permute(combine, PC2, 48)
        rkb.append(round_key)
        rk.append(bin_to_hex(round_key))

#Encrypt
#swap left and right
def swap(left, right):
    a = left
    left = right
    right = a
    return left, right


#Mix one round
def mixxer(left, right, rkb):
    T1 = right
    function()

def function(right, rkb):
    right_expand = permute(right, EP, 48)
    T1 = xor(right_expand, rkb)


def substitute():
    for i in range(1,9):


def encrypt(pt, rkb, rk):
    pt = hex_to_bin(pt)
    pt = permute(pt, IP, 64)
    left = pt[0:32]
    right = pt[32:64]
    for i in range (1, 16):
        mixxer(left, right, rkb)
        if i != 16:
            swap(left, right)
    pre_output = left + right
    ciphertext = permute(pre_output, InvIP, 64)
    return ciphertext

