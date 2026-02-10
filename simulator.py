"""
-------------------------------------------------------------------------------
PROJECT: Heimdall Observability Engine - Simulator
AUTHOR: Alan Padrón
COPYRIGHT: (C) 2026 Alan Padrón. All rights reserved.
-------------------------------------------------------------------------------
"""

import time
import random
from engine import HeimdallEngine

def run_demo():
    engine = HeimdallEngine()
    print("Simulation: Running baseline traffic...")
    
    try:
        # Generar trafico normal
        for _ in range(5):
            engine.monitor(random.randint(100, 120))
            time.sleep(1)
            
        print("\nATTACK INITIATED\n")
        # Generar ataque
        for rps in [1500, 2800, 3200]:
            engine.monitor(rps)
            time.sleep(1)
            
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    run_demo()