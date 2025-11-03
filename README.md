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

## Usage

### CLI

```
└── pyr4t [(--help | -h) | (--version | -V)]                      # Pyr4t CLI
    ├── dev [(--title | -t) <title>]                              # Dev commands
    │   ├── deploy                                                # Deploy project in editable mode with `pip
    │   │                                                           install -e .[dev]`
    │   ├── cls [--cache] [--log] [--tmp]                         # Clean cache, logs and tmp files (choose
    │   │                                                           specific type or all)
    │   ├── dstr                                                  # Check doctring and create/update template
    │   │                                                           if necessary
    │   ├── fmt                                                   # Format scripts in ./src using black and
    │   │                                                           isort
    │   ├── init                                                  # Generate a dev environment in ./dev
    │   └── venv                                                  # Generate a python venv in ./.venv
    ├── package                                                   # Pyr4t package manager
    │   ├── install <package-name>                                # Install a pyr4t package from `R4tL` GitHub
    │   │           [(--version | -V) <package-version>]            repo
    │   └── uninstall <package-name>                              # Uninstall a pyr4t package from local
    │                                                               device
    ├── prod [(--title | -t) <title>]                             # Prod commands
    │   ├── build                                                 # Build production-ready binary
    │   ├── deploy                                                # Deploy project in permanent mode with `pip
    │   │                                                           install .`
    │   ├── run [<script>]                                        # Run a script file from /scripts
    │   └── test                                                  # Run tests
    ├── proj                                                      # Python project manager
    │   ├── add <title> <path> <version>                          # Add a local project to the pyr4t project
    │   │                                                           DB
    │   ├── init (--app | --cli | --lib) <title>                  # Generate a new python project architecture
    │   │        [(--authors | -a) <list-alias>]                    default switch as current
    │   │        [(--path | -p) <path>]
    │   │        [(--version | -V) <proj-version>]
    │   ├── list                                                  # List projects from the pyr4t project DB
    │   ├── modify <title> [(--path | -p) <new-path>]             # Modify project information in the pyr4t
    │   │          [(--version | -V) <new-version>]                 project DB
    │   ├── rm <title>                                            # Remove a project from the pyr4t project DB
    │   ├── whoami                                                # Print the active project in console
    │   └── switch <title>                                        # Switch to another active project from the
    │                                                               pyr4t project DB
    └── user                                                      # User manager
        ├── add <alias> <name> <email>                            # Add a user to the pyr4t user DB
        ├── list                                                  # List users from the pyr4t user DB
        ├── modify <alias> [(--email | -e) <new-email>]           # Modify user information in the pyr4t user
        │          [(--name | -n) <new-name>]                       DB
        ├── rm <alias>                                            # Remove a user from the pyr4t user DB
        ├── switch <alias>                                        # Switch to another active user from the
        │                                                           pyr4t user DB
        └── whoami                                                # Print  the active user in console
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
pyr4t install pyr4tlogger -V 0.1.0
```

NB: all pyr4t package start with `"pyr4t"`.


---

## License

MIT License. See [LICENSE](LICENSE) for details.