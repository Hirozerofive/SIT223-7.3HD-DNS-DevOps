import socket
import json
import sys

SERVER_IP = "127.0.0.1"
SERVER_PORT = 5000


def check_dns_server():
    """Check whether the deployed DNS server is responding correctly."""

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket.settimeout(5)

    query = {
        "hostname": "example.com",
        "query_type": "A"
    }

    try:
        client_socket.sendto(
            json.dumps(query).encode(),
            (SERVER_IP, SERVER_PORT)
        )

        data, _ = client_socket.recvfrom(1024)
        response = json.loads(data.decode())

        if (
            response.get("status") == "success"
            and response.get("ip_address") == "192.168.1.10"
        ):
            print("HEALTH CHECK PASSED")
            print("DNS server is running correctly.")
            return True

        print("HEALTH CHECK FAILED")
        print("Unexpected DNS response.")
        return False

    except socket.timeout:
        print("HEALTH CHECK FAILED")
        print("DNS server did not respond.")
        return False

    finally:
        client_socket.close()


if __name__ == "__main__":
    if check_dns_server():
        sys.exit(0)
    else:
        sys.exit(1)