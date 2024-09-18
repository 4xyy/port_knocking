# Port Knocking Script for macOS

A simple Python-based port knocking security script designed to enhance server security by dynamically opening ports only when a specific sequence of connection attempts is detected.

## Introduction

Port knocking is a security mechanism that allows a server to remain hidden from port scans and only opens specific ports when a correct sequence of "knocks" (connection attempts) is received on designated ports. This script implements a basic port knocking system on macOS, temporarily opening a main service port (e.g., SSH on port 22) upon successful detection of the knock sequence.

## Features

- Listens for a configurable sequence of port knocks.
- Opens a main port (e.g., SSH) only after detecting the correct sequence.
- Uses macOS `pfctl` firewall rules with anchors to manage rules without affecting the main ruleset.

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/<your-username>/port-knocking.git
   cd port-knocking
   sudo python3 port_knocking.py

Usage
Perform the port knock sequence using netcat (nc):
nc -zv 127.0.0.1 1234
nc -zv 127.0.0.1 5678
nc -zv 127.0.0.1 9101

Test SSH Access: After the correct sequence is detected, attempt to connect via SSH:
ssh <username>@127.0.0.1

