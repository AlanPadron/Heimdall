"""
-------------------------------------------------------------------------------
PROJECT: Heimdall Observability Engine - Admin Console
AUTHOR: Alan Padrón
COPYRIGHT: (C) 2026 Alan Padrón. All rights reserved.
IDENTIFIER: HEIMDALL-IAM-MANAGER
-------------------------------------------------------------------------------
DESCRIPTION:
Identity and Access Management (IAM) interface. This tool manages the lifecycle
of technical personnel authorized to receive critical infrastructure logs.
-------------------------------------------------------------------------------
"""

import json
import secrets
import os
from datetime import datetime

DATABASE_FILE = "authorized_techs.json"

def initialize_system():
    """Ensures the technician registry exists before operation."""
    if not os.path.exists(DATABASE_FILE):
        with open(DATABASE_FILE, "w") as f:
            json.dump({"technicians": {}}, f, indent=4)

def fetch_registry():
    with open(DATABASE_FILE, "r") as f:
        return json.load(f)

def commit_changes(data):
    with open(DATABASE_FILE, "w") as f:
        json.dump(data, f, indent=4)

def provision_technician():
    print("\n--- Provision New Technical Personnel ---")
    name = input("Enter technician full name: ")
    department = input("Enter department (SRE/Cybersecurity/Ops): ")
    
    access_token = secrets.token_hex(16)
    
    registry = fetch_registry()
    registry["technicians"][access_token] = {
        "name": name,
        "department": department,
        "status": "active",
        "provisioned_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S") # Formato profesional
    }
    
    commit_changes(registry)
    print(f"\nStatus: Technician {name} successfully provisioned.")
    print(f"Access Token: {access_token}")
    print("Warning: Store this token securely. It will not be displayed again.")
    
    commit_changes(registry)
    print(f"\nStatus: Technician {name} successfully provisioned.")
    print(f"Access Token: {access_token}")
    print("Warning: Store this token securely. It will not be displayed again.")

def deprovision_technician():
    print("\n--- Revoke Access Rights ---")
    token = input("Enter the Token to be revoked: ")
    
    registry = fetch_registry()
    if token in registry["technicians"]:
        tech_identity = registry["technicians"][token]["name"]
        
        # Immediate removal from authorized list
        del registry["technicians"][token]
        
        commit_changes(registry)
        print(f"\nStatus: Access rights for {tech_identity} have been revoked.")
        print("Heimdall Engine will cease log transmissions to this ID immediately.")
    else:
        print("\nError: Token not found in active registry.")

def list_active_personnel():
    print("\n--- Authorized Technical Personnel Registry ---")
    registry = fetch_registry()
    personnel = registry.get("technicians", {})
    
    if not personnel:
        print("Registry is empty. No personnel currently authorized.")
        return

    print(f"{'Token (Prefix)':<15} | {'Name':<20} | {'Dept':<15} | {'Status'}")
    print("-" * 65)
    for token, details in personnel.items():
        print(f"{token[:10]}... | {details['name']:<20} | {details['department']:<15} | {details['status']}")

def main_interface():
    initialize_system()
    while True:
        print("\n" + "="*50)
        print("      HEIMDALL IDENTITY & ACCESS MANAGER")
        print("="*50)
        print("1. Provision New Technician")
        print("2. Audit Active Personnel")
        print("3. Revoke Personnel Access (Deprovision)")
        print("4. Terminate Session")
        
        user_input = input("\nSelect administrative action: ")
        
        if user_input == "1":
            provision_technician()
        elif user_input == "2":
            list_active_personnel()
        elif user_input == "3":
            deprovision_technician()
        elif user_input == "4":
            print("Terminating administrative session...")
            break
        else:
            print("Invalid selection. Please retry.")

if __name__ == "__main__":
    main_interface()