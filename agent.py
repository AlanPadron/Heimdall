import json
import socket
import os

DB_FILE = "authorized_techs.json"
HOST = '127.0.0.1'
PORT = 65432

def authenticate():
    token = input("Enter Security Token: ")
    if not os.path.exists(DB_FILE): return None
    with open(DB_FILE, "r") as f:
        db = json.load(f)
        return db["technicians"].get(token)

def print_formatted_log(log):
    print("="*50)
    print(f"[{log['timestamp']}] ALERT - SEVERITY: {log['severity']}")
    print(f"DIAGNOSIS: {log['diagnosis']}")
    print(f"RPS: {log['metrics']['rps']} | Z-SCORE: {log['metrics']['z_score']}")
    print(f"ACTION: {log['action']}")
    print("="*50 + "\n")

def start_agent():
    user = authenticate()
    if not user:
        print("Access Denied.")
        return

    print(f"\nAGENT ACTIVE: {user['name']} | DEPT: {user['department']}")
    print("System: Waiting for real-time telemetry from Engine...\n")

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen()
        try:
            while True:
                conn, addr = s.accept()
                with conn:
                    data = conn.recv(1024)
                    if data:
                        log = json.loads(data.decode('utf-8'))
                        print_formatted_log(log)
        except KeyboardInterrupt:
            print("\nAgent offline.")

if __name__ == "__main__":
    start_agent()