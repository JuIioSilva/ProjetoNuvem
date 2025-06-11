import socket
import time
import random
import datetime

HOST = '127.0.0.1'
PORT = 5000

def generate_sensor_data():
    umidade = round(random.uniform(40, 70), 2)
    return "Sensor2 - Umidade: {}%".format(umidade)

def log_local(message):
    timestamp = datetime.datetime.now().strftime('%H:%M:%S')
    print("[{}] [Cliente2] {}".format(timestamp, message))

def main():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT))
            log_local("Conectado ao servidor.")
            while True:
                data = generate_sensor_data()
                s.sendall(data.encode())
                resposta = s.recv(1024).decode()
                log_local("Enviado: {}".format(data))
                log_local("Resposta: {}".format(resposta))
                time.sleep(3)
    except ConnectionRefusedError:
        log_local("Erro ao conectar ao servidor.")
    except KeyboardInterrupt:
        log_local("Encerrando cliente.")

if __name__ == "__main__":
    main()
