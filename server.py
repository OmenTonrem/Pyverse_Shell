import socket
import threading
import sys

HOST = "127.0.0.1"
PORT = 12345

def handle_client(client_socket, address):
    """İstemci bağlantısını yönet"""
    print(f"[+] {address} bağlandı.")
    
    try:
        while True:
            # Kullanıcıdan komut al
            command = input(f"Komut ({address}): ").strip()
            
            if not command:
                continue
                
            if command.lower() == 'exit':
                print(f"[-] {address} bağlantısı kapatılıyor...")
                break
            
            # Komutu istemciye gönder
            client_socket.send(command.encode())
            
            # Yanıtı al (büyük çıktılar için)
            response = b""
            while True:
                try:
                    # Socket'i bloke etmeden okuma yap
                    client_socket.settimeout(2.0)
                    chunk = client_socket.recv(4096)
                    if chunk:
                        response += chunk
                    else:
                        break
                except socket.timeout:
                    # Zaman aşımı - daha fazla veri yok
                    break
            
            if response:
                print(f"\n[{address}] Çıktı:\n{response.decode('utf-8', errors='ignore')}")
            else:
                print(f"[{address}] Yanıt alınamadı veya boş.")
                
    except Exception as e:
        print(f"[!] {address} hatası: {e}")
    finally:
        client_socket.close()
        print(f"[-] {address} bağlantısı kapandı.")

def start_server():
    """Sunucuyu başlat"""
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        server.bind((HOST, PORT))
        server.listen(5)
        print(f"[*] Sunucu {HOST}:{PORT} üzerinde dinleniyor...")
        print("[*] 'exit' yazarak istemci bağlantısını kapatabilirsiniz.")
        print("[*] 'quit' yazarak sunucuyu kapatabilirsiniz.\n")
        
        while True:
            client_socket, address = server.accept()
            
            # Yeni istemci için thread oluştur
            client_thread = threading.Thread(
                target=handle_client,
                args=(client_socket, address[0])
            )
            client_thread.daemon = True
            client_thread.start()
            
    except KeyboardInterrupt:
        print("\n[!] Sunucu kapatılıyor...")
    except Exception as e:
        print(f"[!] Sunucu hatası: {e}")
    finally:
        server.close()

def start_single_client_server():
    """Tek istemcili basit sunucu (threadsiz)"""
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        server.bind((HOST, PORT))
        server.listen(1)
        print(f"[*] Sunucu {HOST}:{PORT} üzerinde dinleniyor...")
        print("[*] İstemci bağlanmayı bekliyor...")
        print("[*] 'quit' yazarak çıkış yapabilirsiniz.\n")
        
        client_socket, address = server.accept()
        print(f"[+] {address} bağlandı.")
        
        while True:
            # Kullanıcıdan komut al
            command = input("Komut: ").strip()
            
            if not command:
                continue
                
            if command.lower() == 'quit':
                print("Sunucu kapatılıyor...")
                break
            
            # Komutu istemciye gönder
            client_socket.send(command.encode())
            
            # Yanıtı al
            try:
                client_socket.settimeout(5.0)
                response = client_socket.recv(65536)  # 64KB'ye kadar
                
                if response:
                    print(f"\nÇıktı:\n{response.decode('utf-8', errors='ignore')}")
                else:
                    print("[!] İstemci bağlantısı kesildi.")
                    break
                    
            except socket.timeout:
                print("[!] Yanıt zaman aşımına uğradı.")
            except Exception as e:
                print(f"[!] Hata: {e}")
                break
                
    except KeyboardInterrupt:
        print("\n[!] Sunucu kapatılıyor...")
    except Exception as e:
        print(f"[!] Sunucu hatası: {e}")
    finally:
        try:
            client_socket.close()
        except:
            pass
        server.close()

if __name__ == "__main__":
    print("""
    Sunucu Modu Seçin:
    1. Çoklu istemci (threading)
    2. Tek istemci (basit)
    """)
    
    choice = input("Seçim (1/2): ").strip()
    
    if choice == "1":
        start_server()
    else:
        start_single_client_server()