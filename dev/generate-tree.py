# coding: utf-8


def taille_tree(d, max_len=0):
    """Calcule la longueur max des cles + options + args dans l'arbre."""
    for key, value in d.items():
        opts = ""
        args = ""

        if isinstance(value, dict):
            # Gestion des options
            if "options" in value:
                opts_list = []
                for opt in value["options"]:
                    if isinstance(opt, dict):
                        # Option avec argument
                        opt_str = f"[{opt['name']}]"
                        if "arg" in opt:
                            opt_str += f" <{opt['arg']}>"
                        opts_list.append(opt_str)
                    else:
                        # Option simple
                        opts_list.append(f"[{opt}]")
                opts = " " + " ".join(opts_list)

            # Gestion des args globaux
            if "args" in value:
                args = " " + " ".join(f"<{arg}>" for arg in value["args"])

        total_len = len(key + opts + args)
        if total_len > max_len:
            max_len = total_len

        # Parcours recursif des enfants
        if isinstance(value, dict):
            children = {k: v for k, v in value.items() if isinstance(v, dict)}
            if children:
                max_len = taille_tree(children, max_len)

    return max_len


def print_tree(d, prefix="", level=0, pad=4):
    # Calculer la longueur max des cles + options a ce niveau
    items = list(d.items())
    # max_len = 0
    # for key, value in items:
    #     opts = ""
    #     if isinstance(value, dict) and "options" in value:
    #         opts = " " + " ".join(f"[{opt}]" for opt in value["options"])
    #     args = ""
    #     if isinstance(value, dict) and "args" in value:
    #         args = " " + " ".join(f"<{arg}>" for arg in value["args"])
    #     total_len = len(key + opts + args)
    #     if total_len > max_len:
    #         max_len = total_len
    max_len = taille_tree(commands)
    # Affichage
    for i, (key, value) in enumerate(items):
        connector = "└──" if i == len(items) - 1 else "├──"
        opts = ""
        if isinstance(value, dict) and "options" in value:
            opts_list = []
            for opt in value["options"]:
                if isinstance(opt, dict):
                    # Cas option avec argument
                    opt_str = f"[{opt["name"]}]"
                    if "arg" in opt:
                        opt_str += f" <{opt["arg"]}>"
                    opts_list.append(opt_str)
                else:
                    # Cas simple (string)
                    opts_list.append(f"[{opt}]")
            opts = " " + " ".join(opts_list)
        args = ""
        if isinstance(value, dict) and "args" in value:
            args = " " + " ".join(f"<{arg}>" for arg in value["args"])
        desc = ""
        if isinstance(value, dict) and "description" in value:
            # Ajouter des espaces pour aligner les descriptions
            spaces = " " * (max_len - len(key + opts + args) + pad)
            desc = f"{spaces}# {value['description']}"
        print(f"{prefix}{connector} {key}{args}{opts}{desc}")

        # enfants
        if isinstance(value, dict):
            children = {k: v for k, v in value.items() if k not in ("options", "args", "description")}
            if children:
                extension = "    " if i == len(items) - 1 else "│   "
                print_tree(children, prefix + extension, level + 1, pad)


commands = {
    "pyr4t": {
        "dev": {
            "description": "Dev commands",
            "options": [{"name": "--proj-name", "arg": "proj-name"}],
            "build": {"description": "Build project in editable mode with `pip install -e .[dev]`"},
            "cls": {"description": "Clean cache, logs and tmp files (select an option to chose files to clean just)", "options": ["--cache", "--log", "--tmp"]},
            "docstr": {
                "description": "Check doctring and create/update template if necessary",
            },
            "fmt": {
                "description": "Format scripts in ./src using black and isort",
            },
            "init": {"description": "Generate a dev environment in ./dev"},
            "test": {
                "description": "Lunch all or specific test scripts",
                "options": [{"name": "--test-script", "arg": "test-script"}],
            },
            "venv": {"description": "Generate a python venv in ./.venv"},
        },
        "package": {
            "description": "Pyr4t package manager",
            "install": {"description": "Install a pyr4t package from `R4tL` github repo", "args": ["package-name"]},
            "uninstall": {"description": "Unstall a pyr4t package from local device", "args": ["package-name"]},
            "update": {"description": "Update a pyr4t package on local device", "args": ["package-name"]},
        },
        "prod": {
            "description": "Prod commands",
            "options": [{"name": "--proj-name", "arg": "proj-name"}],
            "build": {
                "description": "Unstall a pyr4t package from local device",
            },
            "run": {"description": "Run __main__.py file"},
            "test": {"description": "Run integration test files"},
        },
        "proj": {
            "description": "Python project manager",
            "add": {"description": "Add a local project to the pyr4t project DB", "args": ["proj-name", "path"]},
            "init": {
                "description": "Generate a new python project architecture (`cli` or `import`)",
                "args": ["proj-type", "proj-name"],
                "options": [{"name": "--authors", "arg": "authors"}, {"name": "--path", "arg": "path"}, {"name": "--version", "arg": "version"}],
            },
            "list": {"description": "List projects from the pyr4t project DB"},
            "modify": {"description": "Modify project informations in the pyr4t project DB", "args": ["proj-name"], "options": ["--name", "--path"]},
            "rm": {"description": "Remove a project from the pyr4t project DB", "args": ["proj-name"]},
            "whoami": {"description": "Print in console the active project"},
            "switch": {"description": "Switch to an other active project from the pyr4t project DB", "args": ["proj-name"]},
        },
        "user": {
            "description": "User manager",
            "add": {
                "description": "Add an user to the pyr4t user DB",
                "args": ["alias"],
                "options": [
                    {"name": "--email", "arg": "email"},
                    {"name": "--name", "arg": "name"},
                ],
            },
            "list": {"description": "List users from the pyr4t user DB"},
            "modify": {
                "description": "Modify user informations in the pyr4t project DB",
                "args": ["alias"],
                "options": [
                    {"name": "--email", "arg": "email"},
                    {"name": "--name", "arg": "name"},
                ],
            },
            "rm": {"description": "Remove an user from the pyr4t project DB", "args": ["alias"]},
            "switch": {"description": "Switch to an other active user from the pyr4t user DB", "args": ["alias"]},
            "whoami": {"description": "Print in console the active user"},
        },
    }
}

print_tree(commands)


# print(taille_tree(commands))
