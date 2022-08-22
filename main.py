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
    i = 13

    while message[i] != 0:
        if message[i] <= 32:
            fqdn = fqdn + '.'
        else:
            fqdn = fqdn + chr(message[i])
        i = i + 1

    reply = ID.to_bytes(2, "big")

    reply += (131).to_bytes(1, "big")
    reply += (0).to_bytes(3, "big")
    reply += (1).to_bytes(2, "big")
    reply += (0).to_bytes(4, "big")
    reply += str.encode(fqdn)
    reply += bytes(64 - len(str.encode(fqdn)))
    reply += (1).to_bytes(2, "big")
    reply += (1).to_bytes(2, "big")
    reply += (10000).to_bytes(4, "big")
    reply += (len("192.168.2.5")).to_bytes(2, "big")
    reply += str.encode("192.168.2.5") + bytes(32 - len("192.168.2.5"))
    print(f'\n\n{reply}')

    UDPServer.sendto(reply, address)

    # print(fqdn)
    # print(host_list)
