import socket
import time
import select

# Client parameters
SERVER_HOST = 'localhost'
SERVER_PORT = 12345
BUFFER_SIZE = 1024
FILENAME = 'test.jpg'
NUM_PACKETS = 10
TIMEOUT_DURATION = 0.0030
MAX_RETRIES = 10
IDLE_TIME = 0.001  # seconds in idle state

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.setblocking(0)

with open(FILENAME, 'rb') as file:
    file_content = file.read()
    print(f"File name {FILENAME} opened")
    packet_size = len(file_content) // NUM_PACKETS
    packets = [file_content[i:i + packet_size] for i in range(0, len(file_content), packet_size)]
    print(f"File {FILENAME} copied to buffer packets")
    if len(file_content) % NUM_PACKETS > 0:
        packets[-1] += file_content[packet_size * NUM_PACKETS:]

rtt_measurements = []

for i, packet in enumerate(packets):
    sequence_number = str(i).zfill(10).encode()
    packet = sequence_number + packet
    ack_received = False
    retry_count = 0

    while not ack_received and retry_count < MAX_RETRIES:
        client_socket.sendto(packet, (SERVER_HOST, SERVER_PORT))
        print(f"Packet {i} sent")
        sent_time = time.perf_counter()

        while True:
            ready = select.select([client_socket], [], [], TIMEOUT_DURATION)
            if ready[0]:
                ack, _ = client_socket.recvfrom(BUFFER_SIZE)
                received_time = time.perf_counter()
                elapsed_time = received_time - sent_time
                rtt_measurements.append(elapsed_time)

                if elapsed_time > TIMEOUT_DURATION:
                    print(f"Timeout occurred for packet {i} after {elapsed_time:.6f} seconds, retrying...")
                    retry_count += 1
                    break

                response = ack.decode()
                if response == f"ACK {i}":
                    ack_received = True
                    print(f"Packet {i} acknowledged, RTT = {elapsed_time:.6f} seconds")
                    break
                elif response == f"NACK {i}":
                    retry_count += 1
                    break
            else:
                print(f"Timeout for packet {i}, retrying...")
                retry_count += 1
                time.sleep(IDLE_TIME)
                break

        if retry_count == MAX_RETRIES:
            print(f"Packet {i} failed after {MAX_RETRIES} retries.")
            break

client_socket.close()

# Calculate the average RTT
if rtt_measurements:
    average_rtt = sum(rtt_measurements) / len(rtt_measurements)
    print(f"Average RTT: {average_rtt:.6f} seconds")
else:
    print("No RTT measurements were made.")
print("File sent.")


