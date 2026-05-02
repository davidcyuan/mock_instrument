"""
fake_instrument_server.py

A TCP server that simulates a lab instrument responding to SCPI commands.
Run this first, then connect to it with instrument_client.py.

Usage:
    python fake_instrument_server.py
"""

import socket
import random
import threading

HOST = "127.0.0.1"
PORT = 5025  # SCPI-raw standard port


class InstrumentState:
    """Holds the simulated instrument's internal state."""

    def __init__(self):
        self.reset()

    def reset(self):
        self.output_enabled = False
        self.power_offset_db = 0.0


def handle_scpi(command: str, state: InstrumentState) -> str | None:
    """
    Parse one SCPI command and return a response string, or None for write-only commands.

    SCPI convention: query commands end with '?', write commands do not.
    """
    command = command.strip().upper()

    if command == "*IDN?":
        return "MockCorp,Model1000,SN-00001,FW-1.0.0"

    if command == "MEAS:POW?":
        # Simulate a noisy power reading in dBm
        base_power = -10.0 + state.power_offset_db
        noise = random.uniform(-0.05, 0.05)
        return f"{base_power + noise:.4f}"

    if command == "MEAS:VOLT?":
        # Simulate a noisy DC voltage reading in volts
        noise = random.uniform(-0.001, 0.001)
        return f"{3.300 + noise:.4f}"

    if command == "*RST":
        state.reset()
        return None  # *RST is a write command — no response

    # Unknown command — real instruments return an error register,
    # but for simplicity we just echo a SCPI-style error string.
    return '-113,"Undefined header"'


def client_session(conn: socket.socket, addr: tuple, state: InstrumentState):
    """Handle one connected client in its own thread."""
    print(f"[server] client connected: {addr}")
    buffer = ""

    try:
        while True:
            chunk = conn.recv(1024)
            if not chunk:
                break
            buffer += chunk.decode()

            # SCPI messages are newline-terminated; a single recv may contain
            # multiple commands or only a partial one.
            while "\n" in buffer:
                line, buffer = buffer.split("\n", 1)
                line = line.strip()
                if not line:
                    continue

                print(f"[server] << {line!r}")
                response = handle_scpi(line, state)

                if response is not None:
                    payload = (response + "\n").encode()
                    conn.sendall(payload)
                    print(f"[server] >> {response!r}")

    except (ConnectionResetError, BrokenPipeError):
        pass
    finally:
        conn.close()
        print(f"[server] client disconnected: {addr}")


def run_server():
    state = InstrumentState()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as srv:
        srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        srv.bind((HOST, PORT))
        srv.listen()
        print(f"[server] listening on {HOST}:{PORT}")
        print("[server] press Ctrl+C to stop\n")

        while True:
            conn, addr = srv.accept()
            # Each client gets its own thread so the server can handle
            # multiple connections, though for this exercise one is enough.
            t = threading.Thread(target=client_session, args=(conn, addr, state), daemon=True)
            t.start()


if __name__ == "__main__":
    run_server()
