import socket
import threading
import datetime

HOST = '127.0.0.1'
PORT = 5000
LOG_FILE = 'log.txt'

def log(message):
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    full_message = "[{}] {}\n".format(timestamp, message)
    with open(LOG_FILE, 'a') as f:
        f.write(full_message)
    print(full_message.strip())

def handle_client(conn, addr):
    log("Nova conexão de {}".format(addr))
    try:
        while True:
            data = conn.recv(1024).decode()
            if not data:
                break
            log("Recebido de {}: {}".format(addr, data))
            conn.sendall("Dados recebidos com sucesso.".encode())
    except Exception as e:
        log("Erro com {}: {}".format(addr, e))
    finally:
        conn.close()
        log("Conexão encerrada com {}".format(addr))

def main():
    log("Servidor iniciando em {}:{}".format(HOST, PORT))
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()

    try:
        while True:
            conn, addr = server.accept()
            thread = threading.Thread(target=handle_client, args=(conn, addr))
            thread.start()
            log("Conexões ativas: {}".format(threading.active_count() - 1))
    except KeyboardInterrupt:
        log("Servidor encerrado manualmente.")
    finally:
        server.close()

if __name__ == "__main__":
    main()
