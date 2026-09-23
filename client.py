import socket
import json

SERVER_IP = "127.0.0.1"
SERVER_PORT = 5000

# Create the UDP client socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.settimeout(5)

print("Mimic DNS client")
print("Make sure the server is running first.")

while True:
    hostname = input("\nEnter a hostname or alias: ").lower()
    query_type = input("Enter the query type (A or CNAME): ").upper()

    # Create the query
    query = {
        "hostname": hostname,
        "query_type": query_type
    }

    try:
        # Send the query to the server
        client_socket.sendto(
            json.dumps(query).encode(),
            (SERVER_IP, SERVER_PORT)
        )

        # Receive the server response
        data, server_address = client_socket.recvfrom(1024)
        response = json.loads(data.decode())

        print("\nResponse received:")

        if response["status"] == "success":

            if response["record_type"] == "A":
                print("Record type: A")
                print("Hostname:", response["hostname"])
                print("IP address:", response["ip_address"])

            elif response["record_type"] == "CNAME":
                print("Record type: CNAME")
                print("Alias:", response["alias"])
                print("Canonical name:", response["canonical_name"])
                print("IP address:", response["ip_address"])

        else:
            print("Error:", response["message"])

    except socket.timeout:
        print("No response received. Make sure the server is running.")

    again = input("\nWould you like to make another query? (yes/no): ")

    if again.lower() not in ["yes", "y"]:
        print("DNS client closed.")
        break

client_socket.close()