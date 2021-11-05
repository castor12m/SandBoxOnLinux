import time
import zmq
import typer

def main(server: bool = False, client: bool = False, clientSend: bool = False, pub: bool = False, sub: bool = False):
    if server:
        typer.echo(f"Use Server")
        DoServer()
    if client:
        typer.echo(f"Use Client")
        DoClient()
    if clientSend:
        typer.echo(f"Use ClientSend")
        DoClientSend()
    if pub:
        typer.echo(f"Use Publisher")
        DoPublisher()
    if sub:
        typer.echo(f"Use Subscriber")
        DoSubscriber()                

def DoServer():
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:5555")

    while True:
        #  Wait for next request from client
        message = socket.recv()
        print("Received request: %s" % message)

        #  Do some 'work'
        time.sleep(1)

        #  Send reply back to client
        socket.send(b"World")
   
def DoClient():
    context = zmq.Context()

    #  Socket to talk to server
    print("Connecting to hello world server…")
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://192.168.0.131:1234")

    #  Do 10 requests, waiting each time for a response
    for request in range(1):
        print("Sending request %s …" % request)
        
        #socket.send(b"Hello from linux")
        udata = '1C 00 C0 00 00 81 00 97 35 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00'
        udataBytes = bytearray.fromhex(udata)
        socket.send(udataBytes)

        #  Get the reply.
        message = socket.recv()
        print("Received reply %s [ %s ]" % (request, message))

def DoClientSend(port = 5555):
    context = zmq.Context()

    #  Socket to talk to server
    print("Connecting to hello world server…1")
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://192.168.0.131:66")

    while True:
        ## 키보드로부터 입력받은 내용을 서버로 전송하고,
        ## 다시 서버의 응답을 출력한다.
        ## bye를 메시지로 보내고 받으면 소켓을 닫는다.
        line = input()

        #socket.send(line.encode())
        udata = '1C 00 C0 00 00 81 00 97 35 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00'
        udataBytes = bytearray.fromhex(udata)
        socket.send(udataBytes)

        rep = socket.recv()
        print(f'Reply: {rep.decode()}')

        if rep.decode() == 'bye':
            socket.close()
            break

def DoPublisher(port = 5555):
    context = zmq.Context()
    sock = context.socket(zmq.PUB)
    #sock.bind("tcp://192.168.0.131:1234")
    #sock.bind("ipc:///tmp/GroundSystem")
    #sock.bind("tcp://*:8000")
    sock.bind("ipc:///tmp/zmq")

    print("Starting loop...")
    i = 1
    while True:
        msg = "Hi for the %d:th time..." % i

        #sock.send_string(msg)
        udata = '1C 00 C0 00 00 81 00 97 35 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00'
        udataBytes = bytearray.fromhex(udata)
        sock.send(udataBytes)

        print("Sent string: %s ..." % msg)
        #i += 1
        time.sleep(1)

    sock.close()
    context.term()

def DoSubscriber(port = 5555):    
    context = zmq.Context()
    sock = context.socket(zmq.SUB)
    #sock.connect("tcp://192.168.0.69:6000")
    #sock.connect("tcp://localhost:8000")
    sock.connect("ipc:///tmp/zmq")
    sock.subscribe("") # Subscribe to all topics

    print("Starting receiver loop ...")
    i = 1
    while i < 5:
        msg = sock.recv()
        print("Received string: %s ..." % msg)

    sock.close()
    context.term()

if __name__ == "__main__":
    typer.run(main)
    