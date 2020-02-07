import clientsock  as cs

def main():
    csock = cs.ClientSocket()
    csock.send(b'test')

if __name__ == '__main__':
    main()