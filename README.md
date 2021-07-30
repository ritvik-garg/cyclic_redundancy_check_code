## **SNS : Lab Assignment-2**

#### Files : 
* client.py
* server.py
* 
#### How to run ?
1. Start the server using command : `python server.py`
2. In multiple terminal tabs, you can create multiple clients connected to the main server, using command : `python client.py`.
3. In every client's window, enter your message which you want to send to the server.
4. After sending the message, clients receive acknowledgement from server, saying whether the message received was correct or not.

#### Note :
1. Divisor polynomial used for calculating CRC remainder is fixed, i.e. x^4+1 (binary : 10001)
2. Cipher matrix used to encode the message at client side is : 
`[[-3, -3, -4], `
`[ 0, 1, 1],`
`[ 4, 3, 4]]`
3. Inverse of cipher matrix used to decode the message at server side is :
`[[1, 0, 1],`
`[4, 4, 3],`
`[-4, -3, -3]]`