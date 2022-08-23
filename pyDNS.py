class pyDNS():

    def __init__(self, query_packet):
        self.query_packet = query_packet
        self.id = int.from_bytes(query_packet[0:2], "big")
        self.fqdn, self.fqdn_with_count = self.getFQDNs(query_packet)
        self.packet_type = self.getPacketType(query_packet)

    def getPacketType(self, packet):
        if int.from_bytes(packet[2:3], "big") == 1:
            packet_type = "Query"
        else:
            packet_type = "Response"
        return packet_type

    def getFQDNs(self, packet):
        i = 12
        fqdn = ''
        fqdn_with_count = ''
        while packet[i] != 0:
            fqdn_with_count += chr(packet[i])
            if i == 12:
                i += 1
                continue
            if packet[i] <= 32:
                fqdn += '.'
            else:
                fqdn += chr(packet[i])
            i += 1
        return fqdn, fqdn_with_count
