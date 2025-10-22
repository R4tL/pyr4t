fichier config: -> si même alias -> erreur, si même nom + email -> erreur, si même path -> erreur
```json
{
    "users": {
        "current": "r4tL",
        "list": {
            "r4tL": {
                "name": "r4tL",
                "email": "simon33910.lambert@gmail.com"
                },
            "yo": {
                "name": "si",
                "email": "m@mail/com"
            }
        }
    },

    "projects": {
        "current": "pyr4t",
        "list": {
            "pyr4t": {
                "path": ""
            }
        }
    }
}
```


LES DIFFERENTS MODULES de "pyr4t"

- dev -> tout ce qui est lié au dev du projet python
- proj -> tout ce qui est lié à la gestions des projets python
- users -> tout ce qui est la gestion des users
- install -> tout ce qui est lié a la gestion des paquets pyr4t
- "rien" -> tout ce qui est lié au projet actuel

1. dev

- init -> creer un environement de dev dans le projet actuel (/dev/tmp, /dev/scripts, /dev/Makefile)
- fmt -> format les scripts dans "src" du projet actuel
- cls -> clean le projet actuel
- venv -> creer  un venv python a la racine du projet actuel
- build -> build le projet actuel en mode editble et avec les req de dev

2. proj

- rm -> remove un projet de la bdd (seulement)
- add -> ajouter un projet local dans la bdd
- list -> list les projets de la bdd
- whoami -> indique quel est le projet actuel

3. user

- list -> lister les user de la bdd
- add -> ajouter un user
- rm -> remove un user
- whoami -> dit qui est le user actuel
- switch -> choisir le user 
- update -> update qqch dans 

4. install / uninstall

- installer / desinstaller un pack pyr4t

5. "rien" (current) (ou --proj-name)

- run -> run le main du projet
- build -> build le projet en prod
- test -> lance les scripts de tests

  
Fait : Pour ça faudrait prendre la taille de la cmd et revenir a la ligne pour les arg si pas la place (comme dans le pyrat proj init)
```
└── pyr4t [(--help | -h) | (--version | -V)]                                             # Pyr4t CLI
    ├── dev [(--proj-title | -t) <proj-title>]                                           # Dev commands
    │   ├── build                                                                        # Build project in editable mode with `pip install -e
    │   │                                                                                  .[dev]`
    │   ├── cls [--cache] [--log] [--tmp]                                                # Clean cache, logs and tmp files (choose specific type or
    │   │                                                                                  all)
    │   ├── docstr                                                                       # Check doctring and create/update template if necessary
    │   ├── fmt                                                                          # Format scripts in ./src using black and isort
    │   ├── init                                                                         # Generate a dev environment in ./dev
    │   └── venv                                                                         # Generate a python venv in ./.venv
    ├── package                                                                          # Pyr4t package manager
    │   ├── install <package-name>                                                       # Install a pyr4t package from `R4tL` GitHub repo
    │   ├── uninstall <package-name>                                                     # Uninstall a pyr4t package from local device
    │   └── update <package-name>                                                        # Update a pyr4t package on local device
    ├── prod [(--proj-title | -t) <proj-title>]                                          # Prod commands
    │   ├── build                                                                        # Build production-ready package or binary
    │   ├── run                                                                          # Run __main__.py file
    │   └── test                                                                         # Run integration or production tests
    ├── proj                                                                             # Python project manager
    │   ├── add <proj-title> <path>                                                      # Add a local project to the pyr4t project DB
    │   ├── init (--app | --cli | --lib) <proj-title> [(--authors | -a) <list-alias>]    # Generate a new python project architecture
    │   │        [(--path | -p) <path>] [(--version | -v) <proj-version>]
    │   ├── list                                                                         # List projects from the pyr4t project DB
    │   ├── modify <proj-title> [(--proj-title | -t) <new-proj-title>]                   # Modify project information in the pyr4t project DB
    │   │          [(--path | -p) <new-path>] (--version | -v) <new-proj-version>]
    │   ├── rm <proj-title>                                                              # Remove a project from the pyr4t project DB
    │   ├── whoami                                                                       # Print the active project in console
    │   └── switch <proj-title>                                                          # Switch to another active project from the pyr4t project
    │                                                                                      DB
    └── user                                                                             # User manager
        ├── add <alias> <name> <email>                                                   # Add a user to the pyr4t user DB
        ├── list                                                                         # List users from the pyr4t user DB
        ├── modify <alias> [(--email | -e) <new-email>] [(--name | -n) <new-name>]       # Modify user information in the pyr4t user DB
        ├── rm <alias>                                                                   # Remove a user from the pyr4t user DB
        ├── switch <alias>                                                               # Switch to another active user from the pyr4t user DB
        └── whoami                                                                       # Print  the active user in console
```

```python
def print_tree(d, prefix=""):
    items = list(d.items())
    for i, (key, value) in enumerate(items):
        connector = "└──" if i == len(items) - 1 else "├──"
        print(f"{prefix}{connector} {key}")
        if isinstance(value, dict):
            extension = "    " if i == len(items) - 1 else "│   "
            print_tree(value, prefix + extension)

# Exemple pour les sous-commandes user
commands = {
    "user": {
        "list": {},
        "add": {"--alias": {}, "--name": {}, "--email": {}},
        "rm": {"<alias>": {}, "--force": {}},
        "whoami": {},
        "switch": {"<alias>": {}},
        "update": {
            "profile": {"<alias>": {}, "--name": {}, "--email": {}},
            "password": {"<alias>": {}, "--password": {}},
        },
    }
}

print_tree(commands)
```

fairz une commande quo créer automatiquement le template de cli avec le json "commands"
pyrat dev code pour ouvrir le projet actuel dans vs code

a faire :
```
my_app/
└── gui/
    ├── __init__.py
    ├── main_window.py      # fenêtre principale
    ├── dialogs.py          # boîtes de dialogue, popups
    ├── widgets.py          # widgets customisés
    └── styles.py           # thèmes, CSS, couleurs
```

```
my_app/
└── api/
    ├── __init__.py
    ├── app.py           # point d’entrée de l’API (FastAPI, Flask)
    ├── routes.py        # définition des endpoints
    ├── dependencies.py  # dépendances, injections de services
    └── schemas.py       # schémas de données (Pydantic)
```