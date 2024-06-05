import threading
import time

cont = 0
valor = 0
x = 2000
lock = threading.Lock()
semaphore = threading.BoundedSemaphore(value=5)


def acesso(numero):
    print(numero, " tentando acesso")
    semaphore.acquire()
    print(numero, " garantido")
    time.sleep(10)
    print(numero, " liberado")
    semaphore.release()

def exThread(message):
    global cont
    for i in range(5):
        cont+=1
        print(message , cont)
        time.sleep(2)
        
def dobro():
    global x, lock
    #lock.acquire()
    while x < 16000:
        x *= 2
        print(x)
        time.sleep(1)
    print("Máximo")
    #lock.release()

def meio():
    global x, lock
    #lock.acquire()
    while x > 1: 
        x /= 2;
        print(x)
        time.sleep(1)
    print("Minimo")
    #lock.release()
    
    
for th_numero in range (1,11):
    t = threading.Thread(target=acesso, args=(th_numero,))
    t.start()
    time.sleep(1)
    
def carrinho(velocidade,nome):
    distancia = 0
    while distancia <= 100:
        print("Carrinho :",nome,distancia)
        distancia += velocidade
        time.sleep(0.3)



carrinho1 = threading.Thread(target=carrinho,args=[1.1,"Ed"])
carrinho2 = threading.Thread(target=carrinho,args=[1.2,"Paulo"])


carrinho1.start()
carrinho2.start()
    
t3 = threading.Thread(target=dobro)
t4 = threading.Thread(target=meio, daemon=True)

t3.start()
t4.start()

t1 = threading.Thread(target=exThread , args=("Thread 1 sendo executada ",))
t2 = threading.Thread(target=exThread , args=("Thread 2 sendo executada ",))
t1.start()
t2.start()
while t1.is_alive() | t2.is_alive() :
    print("Aguardando a Thread " , valor)
    time.sleep(1)
print("Thread morreu")
print("Programa finalizado")