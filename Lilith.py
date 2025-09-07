#!/usr/bin/env python3
# Lilith - Advanced External Security Testing Tool
# By Security Researcher

import os
import sys
import base64
import threading
from queue import Queue
import time

OUTPUT_DIR = "./Lilith_Output"
if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

modules = {
    "file_collector": "Collect files from a specified path",
    "network_monitor": "Simulate network monitoring",
    "info_gather": "Gather system info safely"
}

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

class Lilith:
    def __init__(self):
        self.loaded_module = None
        self.queue = Queue()
        self.logs = []

    def list_modules(self):
        print("Available Modules:")
        for name, desc in modules.items():
            print(f" - {name}: {desc}")

    def use_module(self, module_name):
        if module_name in modules:
            self.loaded_module = module_name
            print(f"[+] Module '{module_name}' loaded")
        else:
            print(f"[!] Module '{module_name}' not found")

    def run_module(self, path=None):
        if not self.loaded_module:
            print("[!] No module loaded")
            return
        if self.loaded_module == "file_collector":
            self.collect_files(path)
        elif self.loaded_module == "network_monitor":
            self.simulate_network()
        elif self.loaded_module == "info_gather":
            self.gather_info()

    def collect_files(self, path):
        if not path or not os.path.exists(path):
            print("[!] Invalid path")
            return
        count = 0
        for root, dirs, files in os.walk(path):
            for file in files:
                try:
                    src = os.path.join(root, file)
                    dst = os.path.join(OUTPUT_DIR, file)
                    with open(src, "rb") as fsrc, open(dst, "wb") as fdst:
                        fdst.write(fsrc.read())
                    count += 1
                except Exception as e:
                    continue
        print(f"[+] {count} files saved in {OUTPUT_DIR}")
        self.logs.append(f"Collected {count} files from {path}")

    def simulate_network(self):
        print("[*] Simulating network monitoring (safe mode)...")
        for i in range(5):
            print(f"[TCP] 192.168.1.{i+1} -> 10.0.2.15 | Port: {1024+i}")
            time.sleep(0.3)
        self.logs.append("Simulated network traffic monitoring")

    def gather_info(self):
        print("[*] Gathering system info safely...")
        info = f"OS: {os.name}, User: {os.getenv('USER') or os.getenv('USERNAME')}"
        print(info)
        self.logs.append(f"System info gathered: {info}")

    def generate_report(self):
        report_file = os.path.join(OUTPUT_DIR, "report.txt")
        with open(report_file, "w") as f:
            for log in self.logs:
                f.write(log + "\n")
        print(f"[+] Report saved as {report_file}")

    def start(self):
        clear_console()
        print("Lilith - Advanced External Security Testing Tool\nType 'help' for commands")
        while True:
            cmd = input("Lilith> ").strip()
            if cmd == "help":
                print("Commands: list, use <module>, run <path>, report, exit")
            elif cmd == "list":
                self.list_modules()
            elif cmd.startswith("use "):
                self.use_module(cmd.split(" ")[1])
            elif cmd.startswith("run"):
                parts = cmd.split(" ", 1)
                path = parts[1] if len(parts) > 1 else None
                self.run_module(path)
            elif cmd == "report":
                self.generate_report()
            elif cmd == "exit":
                print("[*] Exiting Lilith...")
                break
            else:
                print("[!] Unknown command")

if __name__ == "__main__":
    Lilith().start()
