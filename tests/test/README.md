# test v0.1.0

Short description of the project.

---

## Table of Contents

- [About](#about)
- [Python best practices reminder](#python-best-practices-reminder)
- [Installation](#installation)
- [Requirements](#requirements)
- [Usage](#usage)
- [Development](#development)
- [License](#license)

---

## About

* **Version ->** 0.1.0
* **Author ->** me
* **License ->** MIT

---

## Python best practices reminder

* **Create a virtual environment**

```bash
python -m venv .venv
```
* **Activate the pyenv**

- Linux/macOS
```bash
source .venv/bin/activate
```

- Windows
```bash
.venv\Scripts\activate
```

---

## Installation

* **Install directly from GitHub**

- HTTPS
```bash
pip install git+https://github.com/R4tL/test.git@v0.1.0
```

- SSH
```bash
pip install git+ssh://github.com/R4tL/test.git@v0.1.0
```

* **Install directly from Pypi**

```bash
pip install test==0.1.0
```

* **Cloning the repository**

- Classic mode
```bash
pip install .
```

- Editable mode
```bash
pip install -e .
```

- Developpement mode
```bash
pip install -e .[dev]
```

---

## Requirements

### Install `make` (*optional*)

If you want to have acces to the `make` commands.

* **Linux/macOS**
```bash
sudo apt install make # (or brew / xbps-install)
```

* **Windows (with Chocolatey)**

```bash
choco install make
```

---

## Usage

### CLI

* **Run the main project script**

- Integrated CLI
```bash
run-test
```
- Python CLI
```bash
python -m test
```

### Make commands

Go to the root project folder and use the following commands:

* **Build the project for prod**
```bash
make build
```

* **Run test scripts**
```bash
make test
```

### Scripts

Go to the root project folder and use the following commands:

* **Run test scripts**
```bash
python -m scripts.manage -t
```

---

## Development

### Tests

* **Run tests**
```bash
pytest
```

### Make commands

Go to the root project folder and use the following commands:

* **Create a py venv in .venv**
```bash
make -C dev venv
```

* **Build the project in dev mode**
```bash
make -C dev build
```

* **Run the main project**

- Without args
```bash
make -C dev run
```
- With args
```bash
make -C dev run ARGS="arg1 arg2"
```

* **Format the codebase and manage docstrings**

```bash
make -C dev fmt
```

* **Clean files**

- All
```bash
make -C dev clean
```
```bash
make -C dev clean all
```
- Cache only
```bash
make -C dev clean cache
```
- Logs only
```bash
make -C dev clean log
```
- Files in /dev/tmp only
```bash
make -C dev clean tmp
```

### Scripts

Go to the root project folder and use the following commands:

* **Run the main project**

- Without args
```bash
python -m dev.scripts.manage -r
```
- With args
```bash
python -m dev.scripts.manage -r arg1 arg2
```

* **Format the codebase and manage docstrings**

```bash
python -m dev.scripts.manage -f
```

* **Clean files**

- All
```bash
python -m dev.scripts.manage -c
```
```bash
python -m dev.scripts.manage -c all
```
- Cache only
```bash
python -m dev.scripts.manage -c cache
```
- Logs only
```bash
python -m dev.scripts.manage -c log
```
- Files in /dev/tmp only
```bash
python -m dev.scripts.manage -c tmp
```

---

## License

MIT License. See [LICENSE](LICENSE) for details.
