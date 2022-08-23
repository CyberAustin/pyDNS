import socket

UDPServer = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

UDPServer.bind(("0.0.0.0", 44453))

while (True):
    message, address = UDPServer.recvfrom(1024)

    host_list = {"fdsa.com": "192.168.2.3"}

    print(f'\n{message}')
    ID = int.from_bytes(message[0:2], "big")
    print(f'Transaction ID: {ID}')
    print(f'{int.from_bytes(message[2:3], "big")}')

    if int.from_bytes(message[2:3], "big") == 1:
        print("Packet Type: Query")
    else:
        print("Packet Type: Response")

    print(f'Questions: {int.from_bytes(message[3:4], "big")}')

    fqdn = ''
    i = 12
    fqdn_with_count = ''
    while message[i] != 0:
        fqdn_with_count += chr(message[i])
        if i == 12:
            i += 1
            continue
        if message[i] <= 32:
            fqdn += '.'
        else:
            fqdn += chr(message[i])
        i += 1

    #Header ID Field
    reply = ID.to_bytes(2, "big")

    #Header Flags
    reply += (0b10000001).to_bytes(1,"big")
    reply += (0b10000000).to_bytes(1,"big")
    
    reply += (1).to_bytes(2, "big")
    reply += (1).to_bytes(2, "big")
    #print((1).to_bytes(2,"big"))
    
    reply += (0).to_bytes(2, "big")
    reply += (1).to_bytes(2, "big")
    reply += str.encode(fqdn_with_count)
    reply += (0).to_bytes(1, "big")
    reply += (1).to_bytes(2, "big")
    reply += (1).to_bytes(2, "big")
    #print(f'fqdn len: {len(str.encode(fqdn))}')
    #reply += bytes(64 - len(str.encode(fqdn)))
    reply += (0xc00c).to_bytes(2, "big")
    reply += (1).to_bytes(2, "big")
    reply += (1).to_bytes(2, "big")
    reply += (5).to_bytes(4, "big")
    reply += (4).to_bytes(2, "big")

    #ip address
    reply += (192).to_bytes(1, "big")
    reply += (168).to_bytes(1, "big")
    reply += (5).to_bytes(1, "big")
    reply += (8).to_bytes(1, "big")
    reply += (0x0000290fa0000000050000).to_bytes(11, "big")

    
    print(f'\n\n{reply}')

    UDPServer.sendto(reply, address)

    # print(fqdn)
    # print(host_list)
