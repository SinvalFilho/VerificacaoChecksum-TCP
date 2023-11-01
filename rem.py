import socket

# Função para calcular o checksum
def calculate_checksum(data):
    checksum = 0
    for byte in data:
        checksum += byte
        checksum = (checksum & 0xFFFF) + (checksum >> 16)
    return (~checksum) & 0xFFFF

def main():
    # Cria um soquete TCP
    sender_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Define o endereço e a porta do destinatário
    receiver_address = ('localhost', 12312)

    # Estabelece uma conexão com o destinatário
    sender_socket.connect(receiver_address)
    # While para criar um loop.
    while True:
        # Solicita ao usuário que insira a mensagem de texto
        user_input = input("Digite a mensagem de texto (ou 'exit' para encerrar): ")
        
        if user_input == 'exit':
            break

        # Garanta que a mensagem tenha no máximo 16 caracteres (16 bytes)
        user_input = user_input[:16]

        # Preencha a mensagem com espaços em branco para atingir 16 bytes
        user_input = user_input.ljust(16)

        # Codifica a mensagem em bytes
        data_to_send = user_input.encode()

        # Calcula o checksum
        checksum = calculate_checksum(data_to_send)

        # Adiciona o checksum aos dados
        data_to_send += checksum.to_bytes(2, byteorder='big')

        # Envia os dados para o destinatário
        sender_socket.send(data_to_send)

        # Exibe o valor de 16 bits
        print("Valor de 16 bits enviado:", int.from_bytes(data_to_send, byteorder='big'))

        # Aguarda uma resposta (ACK ou NACK) do destinatário
        response = sender_socket.recv(1024)

        if response == b'ACK':
            print("Dados recebidos com sucesso")
        else:
            print("Dados corrompidos. Reenvie-os.")

    # Fecha a conexão com o destinatário
    sender_socket.close()

if __name__ == "__main__":
    main()
