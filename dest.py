import socket

# Função para calcular o checksum
def calculate_checksum(data):
    checksum = 0
    for byte in data:
        checksum += byte
        checksum = (checksum & 0xFFFF) + (checksum >> 16)
    return (~checksum) & 0xFFFF

# Função para verificar o checksum
def verify_checksum(data):
    received_checksum = int.from_bytes(data[-2:], byteorder='big')
    data_without_checksum = data[:-2]
    calculated_checksum = calculate_checksum(data_without_checksum)
    return received_checksum == calculated_checksum

def main():
    # Cria um soquete TCP
    receiver_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Define o endereço e a porta do destinatário
    receiver_address = ('localhost', 12312)

    # Associa o soquete ao endereço
    receiver_socket.bind(receiver_address)

    # Coloca o soquete em modo de escuta para aguardar conexões
    receiver_socket.listen(1)

    # Imprime uma mensagem aguardando a conexão do remetente
    print("Aguardando conexão do remetente...")

    while True:
        # Aceita a conexão do remetente e obtém o soquete do remetente e seu endereço
        sender_socket, sender_address = receiver_socket.accept()

        while True:
            data = sender_socket.recv(1024)

            if not data:
                break

            # Verifica os dados e envia ACK ou NACK ao remetente
            if verify_checksum(data):
                sender_socket.send(b'ACK')
                data_without_checksum = data[:-2]

                # Exibe o valor de 16 bits
                value_16_bits = int.from_bytes(data_without_checksum, byteorder='big')
                print("Valor de 16 bits recebido:", value_16_bits)
                print("Enviando ACK")
            else:
                sender_socket.send(b'NACK')
                print("Dados inválidos recebidos, solicitação de retransmissão")
                print("Enviando NACK")

        sender_socket.close()

if __name__ == "__main__":
    main()
