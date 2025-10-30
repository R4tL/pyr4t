# demo v0.1.0

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
* **Author ->** alice
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
pip install git+https://github.com/a/demo.git@v0.1.0
```

- SSH
```bash
pip install git+ssh://github.com/a/demo.git@v0.1.0
```

* **Install directly from Pypi**

```bash
pip install demo==0.1.0
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

---

## Usage

Go to the root project folder and use the following commands:

### Tests

* **Run the test scripts**
```bash
pytest
```

### Import lib

* **Example**

```python
from demo import Example

ex = Example()
ex.example()
```



---

### Scripts

Go to the root project folder and use the following commands:

* **Run example scripts**
```bash
python -m scripts.manage example
```

---

## License

MIT License. See [LICENSE](LICENSE) for details.
