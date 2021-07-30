import numpy as np

key = "10001"
cipher_matrix = np.array([[-3, -3, -4], [0,1,1], [4,3,4]])
cipher_matrix_inverse = np.array([[1,0,1], [4,4,3], [-4, -3, -3]])

def convertMatrixToString(matrix):
    print ("len : ", len(matrix))
    print ("shape : ", matrix.shape)
    print("matrix[0] : ", matrix[0] )
    res= ""
    for i in range (len(matrix)):
        for j in range(len(matrix[i])):
            if matrix[i][j]!=27:
                char = chr(97+matrix[i][j]-1)
            else:
                char = " "
            res += char

    return res


def parseInput(data):
    data = data[2:-2]
    data = data.strip()
    splitted  = data.split(',')
    matrix = []
    row=[]
    remainder = splitted[-1][2:]
    print("remainder : ", remainder)

    print ("splitted : ", splitted)
    num_cols = len(splitted[:-1])/3

    for w in splitted[:-1] :
        w = w.replace("'", "")
        row.append(int(w))
        if(len(row)==num_cols):
            matrix.append(row)
            row=[]

    return matrix, remainder
        


def convertToString(data):
    res= ""
    for i in range(len(data)):
        for j in range(len(data[i])):
            res = res+str(data[i][j]) + ","
    return res[:-1]

def xor(a,b):
    res = ""
    for i in range(1, len(b)):
        if(a[i]==b[i]):
            res+="0"
        else:
            res+="1"
    return res

def get_remainder(data, divisor):
    selected_data_len = len(divisor)
    temp_data = data[:selected_data_len]

    while selected_data_len<len(data):
        if temp_data[0]=="0":
            dummy = "0" * selected_data_len
            temp_data = xor(dummy, temp_data) + data[selected_data_len]
        else:
            temp_data = xor(divisor, temp_data)+data[selected_data_len]

        selected_data_len+=1

    if temp_data[0]=='1':
        temp_data = xor(divisor, temp_data)
    else:
        dummy = "0" * selected_data_len
        temp_data = xor(dummy, temp_data)

    # return temp_data[]
    return temp_data[-(selected_data_len-1):]


ascii_a = ord('a')

def convertData(data):
    res = ""
    plaintext_matrix = []
    row = []
    for char in data:
        if char==' ':
            res+= format(27, 'b')
            row.append(27)
        else:
            ascii_val = ord(char)
            new_ascii = ascii_val-ascii_a+1
            row.append(new_ascii)
            res+= format(new_ascii, 'b')

        if len(row)==3:
            plaintext_matrix.append(row)
            row=[]

    size_of_matrix = len(plaintext_matrix)

    if len(row) !=0 :
        while(len(row)%3 != 0):
            row.append(27)
        plaintext_matrix.append(row)


    print ("plaintext amatric  ", plaintext_matrix)
    return res, plaintext_matrix

# def convertData(data):

s="dasd fuhaasfda asfda"
print ("len of string : ", len(s))
bin_data, data_matrix = convertData(s)
data_matrix = np.array(data_matrix)
appended_data = bin_data + '0'*(len(key)-1)
remainder = get_remainder(appended_data, key)
encoded_data = np.dot(cipher_matrix, data_matrix.T)
matrix_string = convertToString(encoded_data)
print (bin_data)
print (len(data_matrix))
print (data_matrix)
print (appended_data)
print ("remainder : ", remainder)
print ("encoded data : ", encoded_data)
print ("matrix string : ", matrix_string)

msg_to_server = tuple((matrix_string, remainder))

msg_to_server_str = str(msg_to_server)
print (msg_to_server_str)


new_matrix, remainder_from_client = parseInput(msg_to_server_str)

print ("new matrix : ", new_matrix)
new_matrix = np.array(new_matrix)
print ("new matrix* : ", new_matrix)
print ("remainder from client  : ", remainder_from_client)

decoded_Data = np.dot(cipher_matrix_inverse, new_matrix)
decoded_Data = decoded_Data.T
print ("decoded matrix ; ", decoded_Data)

decoded_msg = convertMatrixToString(decoded_Data)

print ("decoded string : ", decoded_msg)

print ("len of string : ", len(decoded_msg))

decoded_msg = decoded_msg.strip()
print ("new len of string : ", len(decoded_msg))

bin_data_of_decoded_string, data_matrix = convertData(decoded_msg)
appended_data = bin_data_of_decoded_string + '0'*(len(key)-1)

remainder_of_server_String = get_remainder(appended_data, key)

print ("remainder_of_server_String ; ", remainder_of_server_String)

if remainder_from_client == remainder_of_server_String:
    print ("all good man !!! ")
else:
    print ("oops some attacker is here..")

