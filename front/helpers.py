import socket

def get_telemetry():
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    return (local_ip,hostname)