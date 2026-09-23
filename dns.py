import socket
import json

# Server settings
SERVER_IP = "0.0.0.0"  # nosec B104 - required for Docker container networking
SERVER_PORT = 5000

# DNS records
a_records = {
    "example.com": "192.168.1.10",
    "google.com": "142.250.70.14",
    "deakin.edu.au": "128.184.216.21"
}

cname_records = {
    "www.example.com": "example.com",
    "mail.example.com": "example.com"
}


# Function to process DNS queries
def resolve_query(hostname, query_type):
    hostname = hostname.lower()
    query_type = query_type.upper()

    # A record
    if query_type == "A":
        if hostname in a_records:
            return {
                "status": "success",
                "record_type": "A",
                "hostname": hostname,
                "ip_address": a_records[hostname]
            }
        else:
            return {
                "status": "error",
                "message": "A record not found."
            }

    # CNAME record
    elif query_type == "CNAME":
        if hostname in cname_records:
            canonical_name = cname_records[hostname]
            ip_address = a_records[canonical_name]

            return {
                "status": "success",
                "record_type": "CNAME",
                "alias": hostname,
                "canonical_name": canonical_name,
                "ip_address": ip_address
            }
        else:
            return {
                "status": "error",
                "message": "CNAME record not found."
            }

    # Unsupported query
    else:
        return {
            "status": "error",
            "message": "Only A and CNAME queries are supported."
        }


# Start DNS server
def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind((SERVER_IP, SERVER_PORT))

    print("DNS server is running.")
    print(f"Listening on {SERVER_IP}:{SERVER_PORT}")

    while True:
        data, client_address = server_socket.recvfrom(1024)

        try:
            query = json.loads(data.decode())

            hostname = query["hostname"]
            query_type = query["query_type"]

            print("Hostname:", hostname)
            print("Query type:", query_type)

            response = resolve_query(hostname, query_type)

        except (json.JSONDecodeError, KeyError):
            response = {
                "status": "error",
                "message": "Invalid DNS query."
            }

        server_socket.sendto(
            json.dumps(response).encode(),
            client_address
        )


if __name__ == "__main__":
    start_server()