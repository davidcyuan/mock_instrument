"""
instrument_client.py

YOUR job: fill in the blanks marked with TODO using pyvisa.
Read the README first — it explains VISA, SCPI, and pyvisa.

Before running:
    pip install pyvisa pyvisa-py   # pyvisa-py is the pure-Python VISA backend
    python fake_instrument_server.py   # start the fake server in another terminal

Helpful docs:
    https://pyvisa.readthedocs.io/en/latest/
"""

import pyvisa

# ---------------------------------------------------------------------------
# Step 1 — Create a ResourceManager
# ---------------------------------------------------------------------------
# The ResourceManager is pyvisa's entry point. It discovers and manages
# all available VISA resources (instruments).
#
# When you pass no arguments, pyvisa picks a backend automatically.
# The pure-Python backend (pyvisa-py) is fine for TCP/IP instruments.
#
# TODO: create a ResourceManager and assign it to `rm`
#
#   rm = pyvisa.ResourceManager(...)
#
# Hint: to force the pyvisa-py backend use '@py' as the argument.

rm = pyvisa.ResourceManager('@py')


    # ---------------------------------------------------------------------------
    # Step 2 — Open a VISA resource
    # ---------------------------------------------------------------------------
    # VISA identifies instruments with a resource string. For a raw TCP/IP
    # socket instrument the format is:
    #
    #   TCPIP0::<host>::<port>::SOCKET
    #
    # The fake server listens on 127.0.0.1 port 5025, so the resource string is:
    #
    #   "TCPIP0::127.0.0.1::5025::SOCKET"
    #
    # TODO: open the resource and assign it to `instrument`
    #
    #   instrument = rm.open_resource(...)

with rm.open_resource("TCPIP0::127.0.0.1::5025::SOCKET") as instrument:

    # ---------------------------------------------------------------------------
    # Step 3 — Configure the session
    # ---------------------------------------------------------------------------
    # Raw SOCKET resources don't use the VXI-11 protocol, so pyvisa needs to
    # know what character marks the end of each message.
    #
    # TODO: set these two attributes on `instrument`:
    #
    #   instrument.read_termination  = "\n"   # server sends newline-terminated responses
    #   instrument.write_termination = "\n"   # client appends newline to each command
    #
    # These tell pyvisa when to stop reading and what to append when writing.

    instrument.read_termination = "\n"
    instrument.write_termination = "\n"


    # ---------------------------------------------------------------------------
    # Step 4 — Send commands and read responses
    # ---------------------------------------------------------------------------
    # pyvisa gives you three key methods:
    #
    #   instrument.write(cmd)      — send a command, don't wait for a response
    #   instrument.read()          — read one response from the instrument
    #   instrument.query(cmd)      — write then immediately read (most common)
    #
    # TODO: use instrument.query() to send "*IDN?" and print the result.
    # TODO: use instrument.query() to read MEAS:POW? and MEAS:VOLT? and print them.
    # TODO: use instrument.write() to send "*RST" (no response expected).

    print("=== Connecting to fake instrument ===\n")

    print(instrument.query("*IDN?"))
    print(instrument.query("MEAS:POW?"))
    print(instrument.query("MEAS:VOLT?"))


    # ---------------------------------------------------------------------------
    # Step 5 — Close the session
    # ---------------------------------------------------------------------------
    # Always close resources when you're done. Using a `with` block (context
    # manager) is even better — pyvisa closes automatically on exit.
    #
    # TODO: close the instrument and the ResourceManager.
    #
    #   instrument.close()
    #   rm.close()
    #
    # Bonus: rewrite the whole script using:
    #
    #   with rm.open_resource(...) as instrument:
    #       ...