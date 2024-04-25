# Proxy Script

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)  ![Kali](https://img.shields.io/badge/Kali-268BEE?style=for-the-badge&logo=kalilinux&logoColor=white)  ![Ubuntu](https://img.shields.io/badge/Ubuntu-E95420?style=for-the-badge&logo=ubuntu&logoColor=white)

This Python script acts as a simple TCP proxy. It allows you to intercept and modify traffic between a local client and a remote server.

## Usage

To use the script, run it from the command line with the following arguments:

```bash
python3 ./proxy.py [localhost] [localport] [remotehost] [remoteport] [receive_first]
```

- `[localhost]`: The local host IP address.
- `[localport]`: The local port on which the proxy will listen for incoming connections.
- `[remotehost]`: The remote host IP address.
- `[remoteport]`: The port on the remote host to which the traffic will be forwarded.
- `[receive_first]`: Set to `True` if you want the proxy to receive data from the remote host first before forwarding, otherwise set to `False`.

Example:
```bash
python3 ./proxy.py 127.0.0.1 7000 10.7.78.1 8000 True
```

## Screenshot
![](https://github.com/SaherMuhamed/bhp-proxy/blob/main/screenshots/Screenshot_2024-04-25.png)

## Features

- Intercepts TCP traffic between a local client and a remote server.
- Allows packet modification through customizable request and response handlers.
- Provides hex dump functionality for inspecting packet contents.

## How It Works

1. The proxy listens for incoming connections on the specified local port.
2. When a connection is received, it establishes a connection to the remote server.
3. It forwards data between the local client and the remote server, optionally allowing packet inspection and modification.

## Customization

You can customize the behavior of the proxy by modifying the `request_handler` and `response_handler` functions in the script. These functions allow you to perform packet modifications before forwarding them.

## Requirements

- Python 3.x

## Acknowledgement
**This python script provided by Black Hat Python - 2nd Edition book for self learning**
## Disclaimer

This script is provided for educational and testing purposes only. Use it responsibly and ensure that you have appropriate authorization before intercepting and modifying network traffic.

