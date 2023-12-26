import socket
import select
import time

# Server setup
SERVER_HOST = '0.0.0.0'
SERVER_PORT = 12345
BUFFER_SIZE = 1024
NUM_PACKETS = 10
ACK_MSG = "ACK"
NACK_MSG = "NACK"

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((SERVER_HOST, SERVER_PORT))
server_socket.setblocking(0)

print(f"Server listening on {SERVER_HOST}:{SERVER_PORT}")

received_packets = {}
expected_seq_number = 0
processed_seq_numbers = set()

while len(received_packets) < NUM_PACKETS:
    ready = select.select([server_socket], [], [], 5)
    if ready[0]:
        packet, address = server_socket.recvfrom(BUFFER_SIZE)
        sequence_number = int(packet[:10].decode().strip())
        print(f"Packet {sequence_number} received")

        if sequence_number in processed_seq_numbers:
            print(f"Duplicate packet {sequence_number} received. Ignoring.")
            continue

        if sequence_number == expected_seq_number:
            print(f"Buffer [{sequence_number}] copied to file")
            received_packets[sequence_number] = packet[10:]
            expected_seq_number += 1
            server_socket.sendto(f"{ACK_MSG} {sequence_number}".encode(), address)
            print(f"Sent ACK for packet: {sequence_number}")
        else:
            print(f"Received out-of-order packet {sequence_number}. Expected {expected_seq_number}. Sending NACK.")
            server_socket.sendto(f"{NACK_MSG} {sequence_number}".encode(), address)

        processed_seq_numbers.add(sequence_number)

with open('test2.jpg', 'wb') as file:
    for i in range(NUM_PACKETS):
        file.write(received_packets.get(i, b''))
    print(f"Buffer copied to file 'test.jpg'")
server_socket.close()
print("File transfer complete.")
