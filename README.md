# mock_instrument

A learning project for pyvisa — no real hardware needed.

---

## What is VISA?

**VISA** (Virtual Instrument Software Architecture) is a standard API for talking
to test-and-measurement instruments — oscilloscopes, power supplies, signal
generators, etc. It was defined by the IVI Foundation so that the same
application code works regardless of how the instrument is physically connected:

| Transport | Example |
|-----------|---------|
| USB (USBTMC) | Bench instrument via USB cable |
| Ethernet (VXI-11 / HiSLIP / raw TCP) | Instrument on a lab LAN |
| GPIB | Classic HP/Agilent bench gear |
| Serial (RS-232) | Older equipment |

VISA hides those differences behind a single `open_resource / write / read`
interface. You address an instrument by a **resource string** like:

```
TCPIP0::192.168.1.10::5025::SOCKET   ← raw TCP on port 5025
USB0::0x0957::0x0407::MY12345678::INSTR  ← USB instrument
GPIB0::22::INSTR                         ← GPIB address 22
```

---

## What is SCPI?

**SCPI** (Standard Commands for Programmable Instruments, pronounced "skippy")
is a command language that runs on top of VISA. It defines a common vocabulary
so that similar instruments from different vendors behave alike.

Key rules:

- **Commands are ASCII strings**, terminated by a newline.
- **Query commands end with `?`** and return a response.
- **Write commands have no response** (unless an error occurs).
- Commands are hierarchical using `:` as a separator:
  `MEASure:VOLTage:DC?` (often abbreviated to `MEAS:VOLT:DC?`).

Common mandatory commands every SCPI instrument must support:

| Command | Meaning |
|---------|---------|
| `*IDN?` | Return identity string (make, model, serial, firmware) |
| `*RST`  | Reset to factory defaults |
| `*CLS`  | Clear status registers |
| `*OPC?` | Return `1` when all pending operations are complete |

---

## What is pyvisa?

**pyvisa** is a Python library that implements the VISA standard. It lets you
open instrument connections, send SCPI commands, and read responses from Python
without writing any socket or USB code yourself.

```python
import pyvisa

rm = pyvisa.ResourceManager('@py')          # '@py' = pure-Python backend
inst = rm.open_resource('TCPIP0::127.0.0.1::5025::SOCKET')
inst.read_termination  = '\n'
inst.write_termination = '\n'

print(inst.query('*IDN?'))   # → MockCorp,Model1000,SN-00001,FW-1.0.0
inst.close()
rm.close()
```

pyvisa needs a **backend** to do the low-level I/O:

| Backend | When to use |
|---------|-------------|
| **pyvisa-py** (`@py`) | Pure Python — works for TCP, USB, Serial. No drivers needed. Good for learning. |
| NI-VISA | National Instruments driver stack — required for GPIB and some USB instruments in production. |

---

## This project

```
mock_instrument/
├── fake_instrument_server.py   ← TCP server that pretends to be a lab instrument
├── instrument_client.py        ← skeleton for you to fill in using pyvisa
└── README.md                   ← this file
```

### Quick start

```bash
# Terminal 1 — start the fake instrument
python fake_instrument_server.py

# Terminal 2 — fill in instrument_client.py, then run it
pip install pyvisa pyvisa-py
python instrument_client.py
```

### Supported SCPI commands

| Command | Response |
|---------|----------|
| `*IDN?` | Identity string |
| `MEAS:POW?` | Simulated power reading in dBm |
| `MEAS:VOLT?` | Simulated voltage reading in volts |
| `*RST` | Resets state (no response) |

---

## Concepts to be able to explain after this project

1. What problem does VISA solve? (hardware-independent instrument control)  
    VISA allows connections to different types of hardware.

2. What is a VISA resource string and what does each part mean?
    The address to an instrument. For TCP, its TCPIPO::host::port::SOCKET

3. What is the difference between a SCPI query and a write command?  
    query will read something in response to the write. write will only send a command, although you can also try to get back a potential error message

4. What do `read_termination` and `write_termination` do in pyvisa?  
    read_termination: when to stop reading from an instrument
    write_termination: what to append at the end of a write command

5. What is the difference between `write()`, `read()`, and `query()`?  
    write(): send command
    read(): read from instrument, no control
    query(): send command, then read the response to the command

6. Why would you use pyvisa-py vs NI-VISA?  
    Much more lightweight/easy to install
