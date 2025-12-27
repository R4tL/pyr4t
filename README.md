# pyr4t v0.2.0

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

* **Version ->** 0.2.0
* **Author ->** R4tL
* **License ->** MIT

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

### Use `pipx`to install the package globally

```bash
pip install pipx
```
```bash
pipx ensurepath
```
---

## Installation using pip or pipx

* **Install directly from GitHub**

- HTTPS
```bash
pip install git+https://github.com/R4tL/pyr4t.git@v0.2.0
```
```bash
pipx install git+https://github.com/R4tL/pyr4t.git@v0.2.0
```

- SSH
```bash
pip install git+ssh://github.com/R4tL/pyr4t.git@v0.2.0
```
```bash
pipx install git+ssh://github.com/R4tL/pyr4t.git@v0.2.0
```

* **Cloning the repository**

- Classic mode
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
└── pyr4t [(-h | --help) | (-V | --version)]                                  # Pyr4t CLI
    ├── install (--info [p] | <package> [(-V | --version) <version>])         # Install a pyr4t package from R4tL's github repo
    │                                                                           (use '--info' to show all available package)
    ├── init (--app | --cli | --lib) <title>                                  # Generate a new python project architecture,
    │        [(-a | --authors) <alias1> <alias2> ...] [(-p | --path) <path>]    default switch as current
    │        [(-V | --version) <version>]
    ├── build [--prj <title>]                                                 # Build binary files in ./dist (.tar.gz, .whl)
    ├── deploy [--prj <title>] [--dev]                                        # Deploy project using pip (--dev for editable mode)
    ├── run [--prj <title>] [--dev] [<script>]                                # Run a script file from ./scripts (default main.py)
    ├── test [--prj <title>] [<specific>]                                     # Run tests in /tests (default all)
    ├── cls [--prj <title>] [--cache] [--log] [--tmp]                         # Clean cache, logs and tmp files
    ├── dstr [--prj <title>]                                                  # Check doctring and create/update template if
    │                                                                           necessary
    ├── fmt [--prj <title>]                                                   # Format scripts in ./src using black and isort
    ├── venv [--prj <title>]                                                  # Generate a python venv in ./.venv
    ├── dev [--prj <title>]                                                   # Generate dev env in ./dev
    ├── info                                                                  # Print current project informations
    ├── whoami                                                                # Print current user informations
    ├── prj                                                                   # Manage project DB
    │   ├── add <title> <path> <version>                                      # Add a local project to the pyr4t project DB
    │   ├── ls                                                                # List projects from the pyr4t project DB
    │   ├── mv <title> [(-p | --path) <path>] [(-V | --version) <version>]    # Modify project information in the pyr4t project DB
    │   ├── rm <title>                                                        # Remove a project from the pyr4t project DB
    │   └── switch <title>                                                    # Switch to another active project from the pyr4t
    │                                                                           project DB
    └── usr                                                                   # Manage user DB
        ├── add <alias> <name> <email>                                        # Add a user to the pyr4t user DB
        ├── ls                                                                # List users from the pyr4t user DB
        ├── mv <alias> [(-e | --email) <email>] [(-n | --name) <name>]        # Modify user information in the pyr4t user DB
        ├── rm <alias>                                                        # Remove a user from the pyr4t user DB
        └── switch <alias>                                                    # Switch to another active user from the pyr4t user DB
```


NB: all pyr4t package start with `"pyr4t"`.


---

## License

MIT License. See [LICENSE](LICENSE) for details.
