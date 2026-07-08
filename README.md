![tag](https://img.shields.io/github/v/tag/R4tL/pyr4t)
![Python](https://img.shields.io/badge/python-3.13%2B-blue)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![linting: pylint](https://img.shields.io/badge/linting-pylint-yellowgreen)](https://github.com/pylint-dev/pylint)
![License](https://img.shields.io/github/license/R4tL/pyr4t)
[![Documentation](https://img.shields.io/badge/docs-online-blue)](https://R4tL.github.io/pyr4t/)

# pyr4t v1.1.0

A python manager to generate python project architectures, manage them and install pyr4t package based on github: [R4tL repo](https://github.com/R4tL?tab=repositories).
----------------------------------------------------------------------------------------------------------------------------

## Table of Contents

- [About](#about)
- [Documentation](#documentation)
- [Python best practices reminder](#python-best-practices-reminder)
- [Installation](#installation)
- [Usage](#usage)
- [License](#license)

---

## About

* **Version ->** 1.1.0
* **Author ->** [R4tL](https://github.com/R4tL)
* **License ->** MIT

---

## Documentation

- <a href="https://docs.python.org/3/">
  <img src="https://www.python.org/static/img/python-logo.png" alt="Python" width="100" >

</a>

- [Pyr4t](https://r4tl.github.io/pyr4t/)

---

## Python best practices reminder

### Use a Python virtual environment

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

### Use `pipx` to install the package globally

```bash
pip install pipx
```

```bash
pipx ensurepath
```

---

## Installation

Use pip for classic installation.
Use pipx to install the package globally in an isolated environment.

* **Install directly from GitHub**

- HTTPS

```bash
pip install git+https://github.com/R4tL/pyr4t.git@v1.0.1
```

```bash
pipx install git+https://github.com/R4tL/pyr4t.git@v1.0.1
```

- SSH

```bash
pip install git+ssh://git@github.com/R4tL/pyr4t.git@v1.0.1
```

```bash
pipx install git+ssh://git@github.com/R4tL/pyr4t.git@v1.0.1
```

* **Cloning the repository**

Clone the repository on your local machine:

- HTTPS

```bash
git clone https://github.com/R4tL/pyr4t.git@v1.0.1
```

- SSH

```bash
git clone ssh://git@github.com/R4tL/pyr4t.git@v1.0.1
```

Then install the package using pip or pipx:

```bash
pip install .
```

```bash
pipx install .
```

---

## Usage

### CLI

```
└── pyr4t [(-h | --help) | (-V | --version)]                                    # Pyr4t CLI
    ├── install [<package> [(-V | --version) <version>]] [--info]               # Install a pyr4t package from R4tL's github repo
    │           [--info-private] [--token <token>]                                (use '--info(-private)' to show all available
    │                                                                             package)
    ├── init (--app | --cli | --lib) <title>                                    # Generate a new python project architecture, default
    │        [(-a | --authors) <alias1> <alias2> ...] [(-p | --path) <path>]      switched as active project
    │        [(-V | --version) <version>]
    ├── build [(-p | --prj) <title>]                                            # Build binary files in ./dist (.tar.gz, .whl)
    ├── deploy [(-p | --prj) <title>] [(-py | --python) <python-interpreter>]   # Deploy project using pip (--dev for editable mode)
    │          [--dev]
    ├── run [(-p | --prj) <title>] [(-py | --python) <python-interpreter>]      # Run a script file from ./scripts
    │       [--dev] <script> [<script_args>]
    ├── test [(-p | --prj) <title>] [<specific>]                                # Run tests in /tests (default all)
    ├── cls [(-p | --prj) <title>] [--cache] [--log] [--tmp] [<specific>]       # Clean cache, logs and tmp files
    ├── dstr [(-p | --prj) <title>] [<specific>]                                # Check doctring and create/update template if
    │                                                                             necessary
    ├── fmt [(-p | --prj) <title>] [<specific>]                                 # Format scripts in ./src using black and isort
    ├── venv [(-p | --prj) <title>] [(-py | --python) <python-interpreter>]     # Generate a python venv in ./.venv
    │        [--dev]
    ├── dev [(-p | --prj) <title>]                                              # Generate dev env in ./dev
    ├── info                                                                    # Print current project informations
    ├── whoami                                                                  # Print current user informations
    ├── prj                                                                     # Manage project DB
    │   ├── add <title> <path> <version>                                        # Add a local project to the pyr4t project DB
    │   ├── ls                                                                  # List projects from the pyr4t project DB
    │   ├── mv <title> [(-p | --path) <path>] [(-V | --version) <version>]      # Modify project information in the pyr4t project DB
    │   ├── rm <title> [(-f | --files)]                                         # Remove a project from the pyr4t project DB
    │   └── switch <title>                                                      # Switch to another active project from the pyr4t
    │                                                                             project DB
    └── usr                                                                     # Manage user DB
        ├── add <alias> <name> <email>                                          # Add a user to the pyr4t user DB
        ├── ls                                                                  # List users from the pyr4t user DB
        ├── mv <alias> [(-e | --email) <email>] [(-n | --name) <name>]          # Modify user information in the pyr4t user DB   
        ├── rm <alias>                                                          # Remove a user from the pyr4t user DB
        └── switch <alias>                                                      # Switch to another default user from the pyr4t user DB
```

NB: all pyr4t package start with `pyr4t`.

---

## License

MIT License. See [LICENSE](LICENSE) for details.
