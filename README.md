# Viperloop DNS Changer

Viperloop is a simple command-line tool to easily set and reset DNS settings on Linux systems, particularly useful for users in Iran. It is designed to work on most modern Linux distributions that use NetworkManager.

## Easy Installation (Recommended)

For the easiest and safest installation, we recommend using `pipx`. `pipx` installs and runs Python command-line applications in isolated environments, preventing conflicts with system Python packages and other applications.

1.  **Install `pipx`:**
    If you don't have `pipx` installed, you can install it using your system's package manager. For Debian/Ubuntu:
    ```bash
    sudo apt update
    sudo apt install pipx
    ```
    After installing `pipx`, ensure its binaries are accessible in your `PATH` (this is usually done automatically, or you might need to run `pipx ensurepath` and restart your terminal):
    ```bash
    pipx ensurepath
    ```

2.  **Install Viperloop:**
    Once `pipx` is set up, you can install Viperloop directly from GitHub with a single command:
    ```bash
    pipx install git+https://github.com/0CapTaiN0/Viperloop_Linux.git
    ```

Now, you can run the tool from anywhere in your terminal using the `Viperloop` command.

## Alternative Installation (For Developers or Manual Setup)

If you prefer to clone the repository and install manually (e.g., for development), follow these steps. It's highly recommended to use a Python virtual environment to avoid `PEP 668` warnings and potential conflicts with system packages.

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/0CapTaiN0/Viperloop_Linux.git
    cd Viperloop_Linux
    ```

2.  **Create and activate a virtual environment (recommended):**
    ```bash
    python3 -m venv venv
    source venv/bin/activate 
    ```
    (To deactivate the virtual environment later, simply type `deactivate`)

3.  **Install the tool using pip:**
    ```bash
    pip install .
    ```
    If not using a virtual environment and you encounter a `PEP 668` error, you might need to use `pip install . --break-system-packages`, but this is **not recommended** as it can affect your system's Python installation.

## Usage

After installation, you can run the tool from anywhere in your terminal:

```bash
Viperloop
```

This will launch an interactive prompt to set or reset your DNS settings.

## Dependencies

- Python 3.6+
- `psutil`
- `colorama`
- `NetworkManager` enabled on the system

## Contributing

[Details on how to contribute...]

## License

This project is licensed under the CC0-1.0 License. See the [LICENSE](LICENSE) file for details.
