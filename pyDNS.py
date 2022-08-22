class pyDNS():

    def __init__(self, message):
        self.message = message
        self.id = int.from_bytes(message[0:2], "big")

        if int.from_bytes(message[2:3], "big") == 1:
            self.packet_type = "Query"
        else:
            self.packet_type = "Response"
