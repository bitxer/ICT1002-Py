from random import randint, choice, randrange
import numpy as np # also can remove from requirements
import datetime
import os

# remove for integration, created to generate data expected from ML side.

atks = {
 0:'Bot',
 1:'Brute Force -Web',
 2:'Brute Force -XSS', 
 3:'DDOS attack-HOIC',
 4:'DDOS attack-LOIC-UDP',
 5:'DoS attacks-GoldenEye',
 6:'DoS attacks-Hulk', 
 7:'DoS attacks-SlowHTTPTest', 
 8:'DoS attacks-Slowloris',
 9:'FTP-BruteForce',
 10:'Infilteration',
 11:'SQL Injection',
 12:'SSH-Bruteforce'
}



protocol = ['TCP', 'UDP']

port = ['80', '21', '8080', '443', '2701']

def generateisatk():
    return np.random.choice([0,1], p=[0.2, 0.8])

def generateatks(atk):
    if atk == 1:
        return choice(list(atks.values()))
    else:
        return 'Benign'

def generateip():
    return ".".join(str(randint(0, 255)) for _ in range(4))

def generateprotocols():
    return np.random.choice(protocol, p=[0.99, 0.01])

def generateport():
    return choice(port)

def generatetime():
    return randrange(datetime.datetime(2019, 3, 1, 0, 0).timestamp(), datetime.datetime(2020, 3, 1, 0, 0).timestamp())

def run():
    randomdict = {}

    for i in range(0, 100):
        isatk = generateisatk()
        randomdict[i] = {'IsAtk': isatk , 'IP': generateip(), 'Protocol': generateprotocols(), 'Port': generateport(), 'Atk': generateatks(isatk), 'Time': generatetime() }

    f = open('generated.txt', 'w')
    f.write(str(randomdict))
    f.close()

if __name__ == '__main__':
    run()