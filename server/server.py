import socket
from traceback import print_exc
from threading import Thread

KILLCLIENTS = False
DEBUG = False

def debug(msg):
    global DEBUG
    if DEBUG:
        print('DEBUG: {}'.format(msg))

def handle_client(client, addr):
    data = b''
    global KILLCLIENTS
    while True:
        if KILLCLIENTS:
            client.close()
            break
        buf = client.recv(2048)
        if buf == b'bitxer':
            client.close()
            break
        data += buf
    debug('break')
    
def main(hostname='localhost', port=8443):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((hostname, port))
    sock.listen(5)
    print('[+] Sever listening on {}:{}'.format(hostname, port))
    clients = []
    try:
        while True:
            clients = [x for x in clients if x.isAlive()]
            debug(clients)
            try:
                sock.settimeout(10)
                client, addr = sock.accept()
                try:
                    clients.append(Thread(target=handle_client, args=(client, addr)))
                    clients[-1].start()
                except:
                    client.close()
                    print('Error for starting thread for {}:{}'.format(addr[0], addr[1]))
                    print_exc()
            except socket.timeout:
                continue
    except KeyboardInterrupt:
        global KILLCLIENTS
        KILLCLIENTS = True
        while True:
            debug(clients)
            clients = [x for x in clients if x.isAlive()]
            if not clients: break
        sock.close()
        print('[-] Server stopped by user')

if __name__ == '__main__':
    DEBUG = True
    main()