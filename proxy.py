import sys
import socket
import threading

HEX_FILTER = ''.join([(len(repr(chr(i))) == 3) and chr(i) or '.' for i in range(256)])


def main():
    if len(sys.argv[1:]) != 5:
        print("Usage: ./proxy.py [localhost] [localport]", end='')
        print("[remotehost] [remoteport] [receive_first]")
        print("Example: ./proxy.py 127.0.0.1 7000 10.7.78.1 8000 True")
        sys.exit(0)

    local_host = sys.argv[1]
    local_port = int(sys.argv[2])
    remote_host = sys.argv[3]
    remote_port = int(sys.argv[4])
    receive_first = sys.argv[5]

    if "True" in receive_first:
        receive_first = True
    else:
        receive_first = False

    server_loop(
        local_host=local_host,
        local_port=local_port,
        remote_host=remote_host,
        remote_port=remote_port,
        receive_first=receive_first
    )


def hexdump(src, length=16, show=True):
    if isinstance(src, bytes):
        src = src.decode()
    results = list()
    for i in range(0, len(src), length):
        word = str(src[i:i + length])

        printable = word.translate(HEX_FILTER)
        hexa = ' '.join([f'{ord(c):02x}' for c in word])
        hex_width = length * 3
        results.append(f'{i:04x}  {hexa:<{hex_width}}  {printable}')

    if show:
        for line in results:
            print(line)
    else:
        return results


def receive_from(connection):
    buffer = b""
    connection.settimeout(7)
    try:
        while True:
            data = connection.recv(4096)
            if not data:
                break
            buffer += data
    except Exception as e:
        pass
    return buffer


def proxy_handler(client_socket, remote_host, remote_port, receive_first):
    remote_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
    remote_socket.connect((remote_host, remote_port))

    if receive_first:
        remote_buffer = receive_from(connection=remote_socket)
        hexdump(src=remote_buffer)

    remote_buffer = response_handler(buffer=remote_buffer)
    if len(remote_buffer):
        print("[<==] Sending %d bytes to localhost" % len(remote_buffer))
        client_socket.send(remote_buffer)

    while True:
        local_buffer = receive_from(connection=client_socket)
        if len(local_buffer):
            line = "[==>] Received %d bytes to localhost" % len(local_buffer)
            print(line)
            hexdump(src=local_buffer)

            local_buffer = request_handler(local_buffer)
            remote_socket.send(local_buffer)
            print("[==>] Sent to remote")

        remote_buffer = receive_from(connection=remote_socket)
        if len(remote_buffer):
            print("[<==] Received %d bytes from remote" % len(remote_buffer))
            hexdump(src=remote_buffer)

            remote_buffer = request_handler(remote_buffer)
            client_socket.send(remote_buffer)
            print("[<==] Sent to local")

        if not len(local_buffer) or not len(remote_buffer):
            client_socket.close()
            remote_socket.close()
            print("[*] No more data. Closing connections")
            break


def server_loop(local_host, local_port, remote_host, remote_port, receive_first):
    server = socket.socket(family=socket.AF_INET, type=socket.SOCK_STREAM)
    try:
        server.bind((local_host, local_port))
    except Exception as e:
        print("problem on bind: %r" % e)

        print("[!!] Failed to listen on %s:%d" % (local_host, local_port))
        print("[!!] Check for other listening sockets or correct permissions")
        sys.exit(0)

    print("[*] listening on %s:%d" % (local_host, local_port))
    server.listen(7)
    while True:
        client_socket, addr = server.accept()
        print("> Received incoming connection from %s:%d" % (addr[0], addr[1]))

        # start thread to talk to the remote host
        proxy_thread = threading.Thread(
            target=proxy_handler,
            args=(client_socket, remote_host, remote_port, receive_first)
        )
        proxy_thread.start()


def request_handler(buffer):
    # perform packet modifications
    return buffer


def response_handler(buffer):
    # perform packet modifications
    return buffer


if __name__ == "__main__":
    main()
