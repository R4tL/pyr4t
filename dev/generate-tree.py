def print_tree_old(d, prefix=""):
    items = list(d.items())
    for i, (key, value) in enumerate(items):
        connector = "└──" if i == len(items) - 1 else "├──"
        # Affiche les options si elles existent
        opts = ""
        args = ""
        desc = ""
        if isinstance(value, dict) and "options" in value:
            opts = " " + " ".join(f"[{opt}]" for opt in value["options"])
        if isinstance(value, dict) and "args" in value:
            args = " " + " ".join(f"<{arg}>" for arg in value["args"])
        if isinstance(value, dict) and "description" in value:
            desc = f"    # {value["description"]}"
        print(f"{prefix}{connector} {key}{args}{opts}{desc}")
        # Continue récursivement
        if isinstance(value, dict):
            children = {k:v for k,v in value.items() if k not in ["options", "args", "description"]}
            if children:
                extension = "    " if i == len(items) - 1 else "│   "
                print_tree_old(children, prefix + extension)


def print_tree(d, prefix="", level=0, pad=4):
    # Calculer la longueur max des clés + options à ce niveau
    items = list(d.items())
    max_len = 0
    for key, value in items:
        opts = ""
        if isinstance(value, dict) and "options" in value:
            opts = " " + " ".join(f"[{opt}]" for opt in value["options"])
        args = ""
        if isinstance(value, dict) and "args" in value:
            args = " " + " ".join(f"<{arg}>" for arg in value["args"])
        total_len = len(key + opts + args)
        if total_len > max_len:
            max_len = total_len

    # Affichage
    for i, (key, value) in enumerate(items):
        connector = "└──" if i == len(items) - 1 else "├──"
        opts = ""
        if isinstance(value, dict) and "options" in value:
            opts = " " + " ".join(f"[{opt}]" for opt in value["options"])
        args = ""
        if isinstance(value, dict) and "args" in value:
            args = " " + " ".join(f"<{arg}>" for arg in value["args"])
        desc = ""
        if isinstance(value, dict) and "description" in value:
            # Ajouter des espaces pour aligner les descriptions
            spaces = " " * (max_len - len(key + opts) + pad)
            desc = f"{spaces}# {value['description']}"
        print(f"{prefix}{connector} {key}{args}{opts}{desc}")

        # enfants
        if isinstance(value, dict):
            children = {k:v for k,v in value.items() if k not in ("options", "args", "description")}
            if children:
                extension = "    " if i == len(items) - 1 else "│   "
                print_tree(children, prefix + extension, level + 1, pad)



commands = {
    "pyr4t": {
        "dev": {
            "description": "Dev commands",
            "options": ["--proj-name"],
            "build": {
                "description": "Build project in editable mode with `pip install -e .[dev]`"
            },
            "cls": {
                "description": "Clean cache, tmp file and log files args = [`all`, `cache`, `tmp`, `log`]",
                "args": ["file-to-clean"]
            },
            "docstr": {
                "description": "Check doctring and create/update template if necessary",
            },
            "fmt": {
                "description": "Format scripts in ./src using black and isort",
            },
            "init": {
                "description": "Generate a dev environment in ./dev"
            },
            "test": {
                "description": "Lunch all or specific test scripts",
                "options": ["--test-scripts"],
            },
            "venv": {
                "description": "Generate a python venv in ./.venv"
            }
        },
        "package": {
            "install": {
                "description": "Install a pyr4t package from `R4tL` github repo",
                "args": ["package-name"]
            },
            "uninstall": {
                "description": "Unstall a pyr4t package from local device",
                "args": ["package-name"]
            },
            "update": {
                "description": "Update a pyr4t package on local device",
                "args": ["package-name"]
            },
        },
        "prod": {
            "description": "Prod commands",
            "options": ["--proj-name"],
            "build": {
                "description": "Unstall a pyr4t package from local device",
            },
            "run": {},
            "test": {}
        },
        "proj": {
            "add": {
                "args": ["proj-name", "path"]
            },
            "init": {
                "args": ["proj-name"],
                "options": ["--authors", "--path", "--version"]
            },
            "list": {},
            "modify": {
                "args": ["proj-name"],
                "options": ["--name", "--path"]
            },
            "rm": {
                "args": ["proj-name"]
            },
            "whoami": {},
            "switch": {
                "args": ["proj-name"]
            }
        },
        "user": {
            "add": {
                "args": ["alias"],
                "options": ["--email", "--name"]
            },
            "list": {},
            "modify": {
                "args": ["alias"],
                "options": ["--email", "--name"]
            },
            "rm": {
                "args": ["alias"]
            },
            "switch": {
                "args": ["alias"]
            },
            "whoami": {}            
        },
        
    }
}

print_tree(commands)
