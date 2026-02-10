import json
import socket
import statistics
from datetime import datetime

HOST = '127.0.0.1'
PORT = 65432

class HeimdallEngine:
    def __init__(self):
        self.history = [100, 120, 110, 130, 115, 125, 105]
        self.threshold = 3.0

    def calculate_z_score(self, rps):
        mean = statistics.mean(self.history)
        stdev = statistics.stdev(self.history)
        return (rps - mean) / stdev if stdev > 0 else 0

    def generate_log(self, z_score, rps):
        return {
            "timestamp": datetime.now().strftime("%H:%M:%S"),
            "severity": "CRITICAL" if z_score > 5 else "WARNING",
            "diagnosis": "Volumetric DDoS Attack" if z_score > 5 else "Traffic Spike",
            "metrics": {"rps": rps, "z_score": round(z_score, 2)},
            "action": "Immediate firewall rule injection required."
        }

    def broadcast_to_agent(self, log):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(1)
                s.connect((HOST, PORT))
                s.sendall(json.dumps(log).encode('utf-8'))
        except:
            pass

    def monitor(self, rps):
        z = self.calculate_z_score(rps)
        if z > self.threshold:
            log = self.generate_log(z, rps)
            self.broadcast_to_agent(log)
            return log
        else:
            self.history.append(rps)
            if len(self.history) > 50: self.history.pop(0)
            return None