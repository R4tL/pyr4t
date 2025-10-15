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
                "description": "Clean cache, logs and tmp files (select an option to chose files to clean just)",
                "options": ["--cache", "--log", "--tmp"]
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
            "description": "Pyr4t package manager",
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
            "run": {
                "description": "Run __main__.py file"
            },
            "test": {
                "description": "Run integration test files"
            }
        },
        "proj": {
            "description": "Python project manager",
            "add": {
                "description": "Add a local project to the pyr4t project DB",
                "args": ["proj-name", "path"]
            },
            "init": {
                "description": "Generate a new python project architecture (`cli` or `import`), automaticaly added to the DB and slected like active project",
                "args": ["proj-type", "proj-name"],
                "options": ["--authors", "--path", "--version"]
            },
            "list": {
                "description": "List projects from the pyr4t project DB"
            },
            "modify": {
                "description": "Modify project informations in the pyr4t project DB",
                "args": ["proj-name"],
                "options": ["--name", "--path"]
            },
            "rm": {
                "description": "Remove a project from the pyr4t project DB",
                "args": ["proj-name"]
            },
            "whoami": {
                "description": "Print in console the active project"
            },
            "switch": {
                "description": "Switch to an other active project from the pyr4t project DB",
                "args": ["proj-name"]
            }
        },
        "user": {
            "description": "User manager",
            "add": {
                "description": "Add an user to the pyr4t user DB",
                "args": ["alias"],
                "options": ["--email", "--name"]
            },
            "list": {
                "description": "List users from the pyr4t user DB"
            },
            "modify": {
                "description": "Modify user informations in the pyr4t project DB",
                "args": ["alias"],
                "options": ["--email", "--name"]
            },
            "rm": {
                "description": "Remove an user from the pyr4t project DB",
                "args": ["alias"]
            },
            "switch": {
                "description": "Switch to an other active user from the pyr4t user DB",
                "args": ["alias"]
            },
            "whoami": {
                "description": "Print in console the active user"
            }            
        }   
    }
}

print_tree(commands)
