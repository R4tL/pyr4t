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

```
└── pyr4t
    ├── dev [--proj-name]
    │   ├── build
    │   ├── cls
    │   ├── fmt
    │   ├── init
    │   ├── test [--test-script]
    │   └── venv
    ├── package
    │   ├── install <package-name>
    │   ├── uninstall <package-name>
    │   └── update <package-name>
    ├── prod [--proj-name]
    │   ├── build
    │   ├── run
    │   └── test
    ├── proj
    │   ├── add <proj-name> <path>
    │   ├── init <proj-name> [--authors] [--path] [--version]
    │   ├── list
    │   ├── modify <proj-name> [--name] [--path]
    │   ├── rm <proj-name>
    │   ├── whoami
    │   └── switch <proj-name>
    └── user
        ├── add <alias> [--email] [--name]
        ├── list
        ├── modify <alias> [--email] [--name]
        ├── rm <alias>
        ├── switch <alias>
        └── whoami
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