# pyr4t v0.1.0

A python manager to generate python project architectures and install pyr4t package based on github: [R4tL repo](https://github.com/R4tL?tab=repositories).
Look [example](#example-of-usage) to use it.
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
* **Author ->** R4tL
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
.venv\Scripts\\activate
```

---

## Installation

* **Install directly from GitHub**

- HTTPS
```bash
pip install git+https://github.com/R4tL/pyr4t.git@v0.1.0
```

- SSH
```bash
pip install git+ssh://github.com/R4tL/pyr4t.git@v0.1.0
```

* **Install directly from Pypi**

```bash
pip install pyr4t==0.1.0
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

* **Generate a python project achitecture**
```bash
pyr4t profile
```

| Subcommand | Arguments                          | Description                               |
|------------|-----------------------------------|--------------------------------------------|
| list       |                                   | List all profiles                          |
| add        | -a, --alias (required)            | Profile alias                              |
|            | -n, --name (required)             | Profile name                               |
|            | -e, --email (required)            | Profile email                              |
| select     | -a, --alias (required)            | Select a profile as the default            |
| remove     | -a, --alias (required)            | Remove a profile                           |
| update     | -a, --alias (required)            | Alias of the profile to update             |
|            | -n, --name (optional)             | New profile name                           |
|            | -e, --email (optional)            | New profile email                          |
| whoami     |                                   | Show the currently selected profile        |


* **Generate a python project achitecture**
```bash
pyr4t init project-name
```

| Arguments       | Description                                                                  |
| ----------------|------------------------------------------------------------------------------|
| -p, --base_path | Base path where the project will be created (default: current directory)     |
| -v, --version   | Indicate the version of the project (default `"0.1.0"`)                      |
| -a, --authors   | List of authors as `"alias"`, e.g. `--authors "me you bro"` (default `"me"`) |

* **Install a `pyr4t` package**
```bash
pyr4t install pack-name
```

| Arguments       | Description                                                                  |
| ----------------|------------------------------------------------------------------------------|
| -p, --protocol  | Protocol to use for installation (https or ssh) (default `"https"`).         |
| -v, --version   | Indicate the version of the package on github (default `"main"`)             |


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

### Example of usage

1. Create first user
```bash
pyr4t profile add -a "r4tl" -n "R4tL" -e "r4tl@gmail.com"
```
NB: the first user added is automaticaly considerated like the default user (`"me"`).

2. Add collaborator
```bash
pyr4t profile add -a "bro" -n "Jhon" -e "jhon@gmail.com"
```

3. Init a python project
```bash
pyr4t init project -p ./doc/py_projects -v 0.1.0 -a me bro
```

4. You can also install a pyr4t package
```bash
pyr4t install logger -v v0.1.0 -p https
```

NB: all pyr4t package start with `"pyr4t"`. It's not necessary to specify ("pyr4t install pyr4tlogger" works to).


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