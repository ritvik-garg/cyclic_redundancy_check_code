import socket
import sys
import numpy as np

key = "10001"
ascii_a = ord('a')
cipher_matrix = np.array([[-3, -3, -4], [0,1,1], [4,3,4]])
cipher_matrix_inverse = np.array([[1,0,1], [4,4,3], [-4, -3, -3]])

try :
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print ("socket created")
except Exception as e:
    print("Socket cannot be created : ", e)

server_ip = "127.0.0.1"
server_port = 4312
server.connect((server_ip, server_port))

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


    # print ("plaintext amatric  ", plaintext_matrix)
    return res, plaintext_matrix


while True:
    s = input("\n<Enter msg to send to server :> ")
    # s="penguins are one to one"
    print ("len of string : ", len(s))
    bin_data, data_matrix = convertData(s)
    data_matrix = np.array(data_matrix)
    appended_data = bin_data + '0'*(len(key)-1)
    remainder = get_remainder(appended_data, key)
    encoded_data = np.dot(cipher_matrix, data_matrix.T)
    matrix_string = convertToString(encoded_data)
    # print (bin_data)
    # print (len(data_matrix))
    print (data_matrix)
    # print (appended_data)
    # print ("remainder : ", remainder)
    # print ("encoded data : ", encoded_data)
    # print ("matrix string : ", matrix_string)

    msg_to_server = tuple((matrix_string, remainder))

    msg_to_server_str = str(msg_to_server)
    print ("msg to server : ", msg_to_server_str)

    server.send(msg_to_server_str.encode())

    from_server = server.recv(1024).decode()
    print ("<server> : ", from_server)

server.close()