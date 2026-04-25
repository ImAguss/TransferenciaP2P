# TransferenciaP2P

## Project Overview
This is a Peer-to-Peer (P2P) file transfer application built in Python. The project allows users to send and receive files directly between computers using TCP sockets. 

The architecture is divided into two main components:
*   **Emisor (Sender):** Responsible for connecting to a specified IP address and port, sending a JSON header with file metadata (name, size, type), and then streaming the file contents in chunks. (`src/core/emisor.py`)
*   **Receptor (Receiver):** Acts as a server listening for incoming connections. It receives the metadata header, prompts the user to accept the transfer, and then receives and saves the file chunks to a specified destination folder. (`src/core/receptor.py`)

The application includes a command-line interface with a Tkinter-based file selection dialog (`src/main.py`).

## Building and Running

### Prerequisites
*   Python 3.x
*   Tkinter (usually included with standard Python installations, required for the file selection dialog).

### Running the Application
To start the interactive menu for sending or receiving files:
```bash
python src/main.py
```
*   Select `1` to act as an Emisor (Sender). You will be prompted to select a file using a GUI dialog and enter the destination IP.
*   Select `2` to act as a Receptor (Receiver). You will be prompted to enter a destination path where received files will be saved. The application will then listen for incoming connections on port 5000 (default).

### Running Tests
The project includes an automated test script that mocks the transfer process locally (using localhost).
```bash
python tests/test_automatizado.py
```

## Development Conventions
*   **Path Manipulation:** The project uses the standard `pathlib` library for handling file paths, ensuring cross-platform compatibility.
*   **Network Protocol:** Custom application-level protocol over TCP. Transfers start with a 4-byte packed integer indicating the size of the subsequent JSON header, followed by the JSON header with file metadata, and finally the raw file bytes streamed in 1024-byte chunks.
*   **Concurrency:** The `main.py` utilizes the `threading` module to start the server in the background, allowing the application to wait for connections without completely blocking execution.
*   **Language:** Python (Standard library only used, no external pip dependencies identified so far).

## Agent Instructions
*   **Role:** Act as a reviewer and assistant.
*   **File Modifications:** DO NOT modify any files directly (unless explicitly asked to). Only read files, analyze the code, and provide suggestions, advice, or code snippets for the user to apply manually.
