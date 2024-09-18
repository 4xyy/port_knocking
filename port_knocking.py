import socket
import threading
import os
import logging

# Configuration
KNOCK_SEQUENCE = [1234, 5678, 9101]  # Sequence of ports to knock
MAIN_PORT = 22                       # Port to open after correct knock (e.g., SSH)
TIMEOUT = 10                         # Time window in seconds for the correct sequence
OPEN_PORT_DURATION = 60              # Time in seconds for which the main port stays open

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

# Global variables
knock_attempts = []
lock = threading.Lock()

def listen_on_port(port):
    """Listen on a specific port for knock attempts."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind(("0.0.0.0", port))
            s.listen(1)
            s.settimeout(TIMEOUT)
            logging.info(f"Listening on port {port}...")
            conn, addr = s.accept()  # Accept the connection
            with conn:
                logging.info(f"Knock on port {port} from {addr}")
                with lock:
                    knock_attempts.append(port)
        except Exception as e:
            logging.error(f"Error on port {port}: {e}")

def monitor_knocks():
    """Monitor knock attempts and verify if they match the correct sequence."""
    while True:
        with lock:
            if knock_attempts == KNOCK_SEQUENCE:
                logging.info("Correct knock sequence detected! Opening main port.")
                open_main_port()
                knock_attempts.clear()
                threading.Timer(OPEN_PORT_DURATION, close_main_port).start()
            elif len(knock_attempts) > len(KNOCK_SEQUENCE) or (
                len(knock_attempts) > 0 and knock_attempts != KNOCK_SEQUENCE[:len(knock_attempts)]
            ):
                logging.warning("Incorrect sequence. Resetting knocks.")
                knock_attempts.clear()

def open_main_port():
    """Open the main port using firewall rules."""
    os.system("echo 'pass in proto tcp from any to any port 22' | sudo pfctl -a 'knock/ssh' -f -")  # Add rule to the anchor
    os.system("sudo pfctl -a 'knock/ssh' -e")  # Enable the anchor
    logging.info("Main port opened.")

def close_main_port():
    """Close the main port after it was temporarily opened."""
    logging.info("Closing main port.")
    os.system("sudo pfctl -a 'knock/ssh' -F all")  # Flush rules from the specific anchor

def main():
    # Start monitoring thread
    threading.Thread(target=monitor_knocks, daemon=True).start()

    # Start listeners on all knock ports
    listeners = [threading.Thread(target=listen_on_port, args=(port,), daemon=True) for port in KNOCK_SEQUENCE]

    for listener in listeners:
        listener.start()

    for listener in listeners:
        listener.join()

if __name__ == "__main__":
    main()
