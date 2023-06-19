import socket
import threading
import time

def receive_message(sock):
    buffer_size = 4096
    data = sock.recv(buffer_size)
    if not data:
        return None
    return data.decode()

def send_battery_status(new_sock, battery):
    while True:
        new_sock.send(f"B{battery[0]}".encode())
        time.sleep(1)  

def decrement_battery(battery):
    while True:
        if battery[0] > 10:
            battery[0] -= 1
        if battery[0] <= 10:
            battery[0] = 100
        time.sleep(1)  

def main():
    listen_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listen_sock.bind(("0.0.0.0", 8080))
    listen_sock.listen(3)
    
    battery = [100]

    while True:
        print("\nWaiting for a connection...\n")
        new_sock, address = listen_sock.accept()
        
        host, port = address
        print(f"Connected with {host}:{port}")
        
        # Start new threads to continuously send battery status updates and decrement battery value
        threading.Thread(target=send_battery_status, args=(new_sock, battery)).start()
        threading.Thread(target=decrement_battery, args=(battery,)).start()

        while True:
            message = receive_message(new_sock)
            if message is None:
                break

            print("MESSAGE:", message)

        new_sock.close()
        
    listen_sock.close()

if __name__ == "__main__":
    main()
