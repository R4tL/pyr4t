import shutil
import pyr4tlogger

import shutil

LOG = pyr4tlogger.LoggerManager(__file__, log_dir_base=r"C:\Users\sim33\Documents\projects\pyr4t\dev").logger

# FIXME -> si y'a une desc trop longue au premier du tree ca met pas les lignes :
# └── pyr4t                                                         # Dev jfir iuejfoierj oifj er ifj oire jf
#                                                                     reifj  froij ef roifj e foeir f
#     ├── dev [--proj-name] <proj-name>                             # Dev commands gjg jgnrgn gugu gun ngn, d l
#     │                                                               kb kb rtlg rtlkg rlgk rglk trlg rtglkrt
#     │   ├── build                                                 # Build project in editable mode with `pip
#     │   │                                                           install -e .[dev]`
# + -> vu qu'on trie par mot et que le mot est trop long (plus long que desc width) ca revient mal a la ligne

def wrap_sequence(prefix: str, connector: str, key: str, seq_list: list[str], desc = ""):

    # Init term dimentions
    term_width = shutil.get_terminal_size().columns
    desc_width = 2*term_width // 5 
    max_width = term_width - desc_width
    
    # Init variable for code
    desc_split = wrap_desc(desc, desc_width)
    base_line = f"{prefix}{connector} {key}"
    wrap_connector = "│   " if connector == "├──" else "    "
    indent = " " * (len(base_line) + 1 - len(prefix + wrap_connector))
    lines = []
    current_line = base_line

    # Cheack if we can append each elt on one line
    for elem in seq_list:
        elem_str = f" {elem}"
        if len(current_line) + len(elem_str) > max_width -1:
            # Create a line with this content and we will create a new
            if desc_split: # add desc
                spaces = " " * (max_width - len(current_line))
                current_line += f"{spaces}{desc_split.pop(0)}"
            lines.append(current_line)
            current_line = prefix + wrap_connector + indent + elem.strip() # create new line
        else:
            # Can spread on one line
            current_line += elem_str

    # Last line
    if desc_split:
        spaces = " " * (max_width - len(current_line))
        current_line += f"{spaces}{desc_split.pop(0)}"
    lines.append(current_line)
    for line_desc in desc_split:
        spaces = " " * ((max_width)-len(prefix + wrap_connector))
        lines.append(prefix + wrap_connector + spaces + line_desc)

    return lines

def wrap_desc(desc: str, desc_width: int):

    words = desc.split(" ")
    lines = []
    current_line = ""
    for word in words:
        # +1 for the space between words if it's not the first word in the line
        extra_len = len(word) + (1 if current_line else 0)
        if len(current_line) + extra_len > desc_width:
            # Line is full -> append it to lines
            lines.append(current_line)
            # For subsequent lines, add indentation
            current_line = "  " + word
        else:
            # Add the word to the current line
            if current_line:
                current_line += " " + word
            else:
                current_line = word
    if current_line:
        lines.append(current_line)
    return lines


def build_lines(dict_cmd: dict, prefix=""):

    lines = []
    items = list(dict_cmd.items())
    for i, (key, value) in enumerate(items):
        connector = "└──" if i == len(items) - 1 else "├──"
        seq_list = value.get("__seq__", [])
        desc = value.get("__desc__", "")
        if desc:
            desc = "# " + desc
        wrapped_lines = wrap_sequence(prefix, connector, key, seq_list, desc)
        lines.extend(wrapped_lines)
        children = {
            k: v for k, v in value.items()
            if isinstance(v, dict) and k not in ("__seq__", "__desc__")
        }
        if children:
            extension = "    " if i == len(items) - 1 else "│   "
            lines.extend(build_lines(children, prefix + extension))
    return lines


def print_tree(dict_cmd):
    lines = build_lines(dict_cmd)
    for line in lines:
        print(line)



def main(cmd):
    print_tree(cmd)



commands = {
    "pyr4t": {
        "dev": {
            "__desc__": "Dev commands",
            "__seq__": ["[--proj-name] <proj-name>"],
            "build": {
                "__desc__": "Build project in editable mode with `pip install -e .[dev]`",
            },
            "cls": {
                "__desc__": "Clean cache, logs and tmp files (choose specific type or all)",
                "__seq__": ["[--cache]", "[--log]", "[--tmp]"],
            },
            "docstr": {
                "__desc__": "Check doctring and create/update template if necessary",
            },
            "fmt": {
                "__desc__": "Format scripts in ./src using black and isort",
            },
            "init": {
                "__desc__": "Generate a dev environment in ./dev",
            },
            "test": {
                "__desc__": "Launch all or specific test scripts",
                "__seq__": ["[--test-script] <test-script>"],
            },
            "venv": {
                "__desc__": "Generate a python venv in ./.venv"
            },
        },

        "package": {
            "__desc__": "Pyr4t package manager",
            "install": {
                "__desc__": "Install a pyr4t package from `R4tL` GitHub repo",
                "__seq__": ["<package-name>"],
            },
            "uninstall": {
                "__desc__": "Uninstall a pyr4t package from local device",
                "__seq__": ["<package-name>"],
            },
            "update": {
                "__desc__": "Update a pyr4t package on local device",
                "__seq__": ["<package-name>"],
            },
        },

        "prod": {
            "__desc__": "Prod commands",
            "__seq__": ["[--proj-name] <proj-name>"],
            "build": {
                "__desc__": "Build production-ready package or binary",
            },
            "run": {
                "__desc__": "Run __main__.py file",
            },
            "test": {
                "__desc__": "Run integration or production tests",
            },
        },

        "project": {
            "__desc__": "Python project manager",
            "add": {
                "__desc__": "Add a local project to the pyr4t project DB",
                "__seq__": ["<proj-name>", "<path>"],
            },
            "init": {
                "__desc__": "Generate a new python project architecture (`cli`, `app`, or `lib`)",
                "__seq__": [
                    "(--app | --cli | --lib)",
                    "<proj-name>",
                    "[--authors] <authors>",
                    "[--path] <path>",
                    "[--version] <version>"
                ],
            },
            "list": {
                "__desc__": "List projects from the pyr4t project DB",
            },
            "modify": {
                "__desc__": "Modify project information in the pyr4t project DB",
                "__seq__": ["<proj-name>", "[--name] <name>", "[--path] <path>"],
            },
            "rm": {
                "__desc__": "Remove a project from the pyr4t project DB",
                "__seq__": ["<proj-name>"],
            },
            "whoami": {
                "__desc__": "Print in console the active project",
            },
            "switch": {
                "__desc__": "Switch to another active project from the pyr4t project DB",
                "__seq__": ["<proj-name>"],
            },
        },

        "user": {
            "__desc__": "User manager",
            "add": {
                "__desc__": "Add a user to the pyr4t user DB",
                "__seq__": [
                    "<alias>",
                    "[--email] <email>",
                    "[--name] <name>",
                ],
            },
            "list": {
                "__desc__": "List users from the pyr4t user DB",
            },
            "modify": {
                "__desc__": "Modify user information in the pyr4t user DB",
                "__seq__": [
                    "<alias>",
                    "[--email] <email>",
                    "[--name] <name>",
                ],
            },
            "rm": {
                "__desc__": "Remove a user from the pyr4t user DB",
                "__seq__": ["<alias>"],
            },
            "switch": {
                "__desc__": "Switch to another active user from the pyr4t user DB",
                "__seq__": ["<alias>"],
            },
            "whoami": {
                "__desc__": "Print in console the active user",
            },
        },
    }
}

commands2_test = {
    "pyr4t": {
        "dev": {

            "__seq__": ["[--proj-name] <proj-name>"],
            "build": {

            },
            "cls": {

                "__seq__": ["[--cache]", "[--log]", "[--tmp]"],
            },
            "docstr": {

            },
            "fmt": {

            },
            "init": {

            },
            "test": {

                "__seq__": ["[--test-script] <test-script>"],
            },
            "venv": {

            },
        },

        "package": {

            "install": {

                "__seq__": ["<package-name>"],
            },
            "uninstall": {

                "__seq__": ["<package-name>"],
            },
            "update": {

                "__seq__": ["<package-name>"],
            },
        },

        "prod": {

            "__seq__": ["[--proj-name] <proj-name>"],
            "build": {

            },
            "run": {

            },
            "test": {

            },
        },

        "project": {

            "add": {

                "__seq__": ["<proj-name>", "<path>"],
            },
            "init": {

                "__seq__": [
                    "(--app | --cli | --lib)",
                    "<proj-name>",
                    "[--authors] <authors>",
                    "[--path] <path>",
                    "[--version] <version>"
                ],
            },
            "list": {

            },
            "modify": {

                "__seq__": ["<proj-name>", "[--name] <name>", "[--path] <path>"],
            },
            "rm": {

                "__seq__": ["<proj-name>"],
            },
            "whoami": {

            },
            "switch": {

                "__seq__": ["<proj-name>"],
            },
        },

        "user": {

            "add": {

                "__seq__": [
                    "<alias>",
                    "[--email] <email>",
                    "[--name] <name>",
                ],
            },
            "list": {

            },
            "modify": {

                "__seq__": [
                    "<alias>",
                    "[--email] <email>",
                    "[--name] <name>",
                ],
            },
            "rm": {

                "__seq__": ["<alias>"],
            },
            "switch": {

                "__seq__": ["<alias>"],
            },
            "whoami": {

            },
        },
    }
}

main(commands)




