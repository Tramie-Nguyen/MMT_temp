import socket
import hashlib
import os
import threading

HOST = '127.0.0.1'  # Server IP address
PORT = 65432        # Server port
BUFFER_SIZE = 4096
FORMAT = "utf-8"

# Global variable to track if upload is stopped
upload_stopped = False

def get_file_parts(file_path, part_size):
    with open(file_path, "rb") as f:
        while True:
            part = f.read(part_size)
            if not part:
                break
            yield part

def send_file(file_path, part_size=BUFFER_SIZE):
    global upload_stopped

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))

    file_name = os.path.basename(file_path)
    client_socket.send(file_name.encode(FORMAT))

    response = client_socket.recv(BUFFER_SIZE).decode(FORMAT)
    if response != "READY":
        print("Server not ready")
        client_socket.close()
        return

    parts = list(get_file_parts(file_path, part_size))
    total_parts = len(parts)
    client_socket.send(str(total_parts).encode(FORMAT))

    ack = client_socket.recv(BUFFER_SIZE).decode(FORMAT)
    if ack != "ACK":
        print("Server did not acknowledge total parts")
        client_socket.close()
        return

    for index, part in enumerate(parts):
        if upload_stopped:
            print("Upload stopped by user.")
            break
        
        part_hash = hashlib.md5(part).hexdigest()
        client_socket.send(f"{index}".encode(FORMAT))
        client_socket.recv(BUFFER_SIZE)
        client_socket.send(part_hash.encode(FORMAT))
        client_socket.recv(BUFFER_SIZE)
        client_socket.sendall(part)
        response = client_socket.recv(BUFFER_SIZE).decode(FORMAT)
        if response != "ACK":
            print(f"Error in sending part {index}")
            break

    client_socket.close()

def stop_upload():
    global upload_stopped
    upload_stopped = True

if __name__ == "__main__":
    file_path = "path_to_large_file.jpg"
    
    # Start a separate thread for uploading the file
    upload_thread = threading.Thread(target=send_file, args=(file_path,))
    upload_thread.start()

    # Simulate some delay before stopping the upload (for demonstration)
    time.sleep(5)

    # Stop the upload process
    stop_upload()

    # Wait for the upload thread to complete
    upload_thread.join()


def download_file(file_name):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))

    client_socket.send(f"/download/{file_name}".encode(FORMAT))

    response = client_socket.recv(BUFFER_SIZE).decode(FORMAT)
    if response == "FILE_NOT_FOUND":
        print("File not found on server")
        client_socket.close()
        return

    # Assuming server sends the file size first
    file_size = int(response)
    received = 0

    download_path = os.path.join(os.getcwd(), 'downloads', file_name)  # Download to 'downloads' folder locally
    os.makedirs(os.path.dirname(download_path), exist_ok=True)

    with open(download_path, 'wb') as f:
        while received < file_size:
            data = client_socket.recv(BUFFER_SIZE)
            if not data:
                break
            f.write(data)
            received += len(data)

    print(f"File {file_name} downloaded successfully to {download_path}")

    client_socket.close()

if __name__ == "__main__":
    file_name_to_download = "example_file.txt"  # Replace with the file you want to download
    download_file(file_name_to_download)
