import socket
from traceback import print_exc
from threading import Thread
from modules.parser import Parser
KILLCLIENTS = False
DEBUG = False
EOT = b'bitxer'

def debug(msg):
    global DEBUG
    if DEBUG:
        print('DEBUG: {}'.format(msg))

def new_zip(data, filetype=0):
    # Handle zip file uploads
    pass

def new_file(data, filetype):
    # Handle non zip file uploads
    data = data.decode()
    reader = Parser.Reader(data, filetype)
    df = reader.read()
    # Input dataframe to ml function

def handle_client(client, addr):
    global KILLCLIENTS
    global EOT
    data = b''
    action = 0
    filetype = 0
    first = True
    second = False
    actions = {1 :new_zip, 2: new_file}
    while True:
        if KILLCLIENTS:
            client.close()
            # break
        
        buf = client.recv(2048)
        try:
            if first:
                action = actions[buf]
                second = True
        except:
            debug('Invalid action provided')
            client.send(b'Invalid action provided.')
            client.close()
        finally:
            if second:
                filetype = buf

            if buf == EOT:
                debug('Transmission ended')
                client.close()
                break

            if not first and not second:
                data += buf
            else:
                first = action == 0
                second = filetype == 0
    action(data, filetype)

    # debug('break')
    
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