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
└── pyr4t [(--help | -h) | (--version | -V)]                                         
    ├── dev [(--proj-title | -t) <proj-title>]                                       
    │   ├── build                                                                    
    │   │                                                                            
    │   ├── cls [--cache] [--log] [--tmp]                                            
    │   │                                                                            
    │   ├── docstr                                                                   
    │   ├── fmt                                                                      
    │   ├── init                                                                     
    │   └── venv                                                                     
    ├── package                                                                      
    │   ├── install <package-name>                                                   
    │   ├── uninstall <package-name>                                                 
    │   └── update <package-name>                                                    
    ├── prod [(--proj-title | -t) <proj-title>]                                      
    │   ├── build                                                                    
    │   ├── run <script>  # dans la bdd on a les path des scripts a run EN UTILISANT LE PATH SCRIPT                                                         
    │   └── test                                                                     
    ├── proj                                                                         
    │   ├── add <proj-title> <path>                                                  
    │   ├── init (--app | --cli | --lib) <proj-title> [(--authors | -a) <list-alias>]
    │   │        [(--path | -p) <path>] [(--version | -v) <proj-version>]
    │   ├── list                                                                     
    │   ├── modify <proj-title> [(--proj-title | -t) <new-proj-title>]               
    │   │          [(--path | -p) <new-path>] (--version | -v) <new-proj-version>]
    │   ├── rm <proj-title>                                                          
    │   ├── whoami                                                                   
    │   └── switch <proj-title>                                                      
    │                                                                                
    └── user                                                                         
        ├── add <alias> <name> <email>                                               
        ├── list                                                                     
        ├── modify <alias> [(--email | -e) <new-email>] [(--name | -n) <new-name>]   
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


github json:
```
{
  "url": "https://api.github.com/repos/username/repo/releases/123456",
  "tag_name": "v0.2.0",
  "name": "v0.2.0",
  "assets": [
    {
      "id": 987654,
      "name": "pyr4tlogger-0.2.0-py3-none-any.whl",
      "browser_download_url": "https://github.com/username/repo/releases/download/v0.2.0/pyr4tlogger-0.2.0-py3-none-any.whl",
      "size": 123456
    },
    {
      "id": 987655,
      "name": "pyr4tlogger-0.2.0.tar.gz",
      "browser_download_url": "https://github.com/username/repo/releases/download/v0.2.0/pyr4tlogger-0.2.0.tar.gz",
      "size": 234567
    }
  ]
}
```

POUR pakcage downgrade: changer le nom pour que ça soit juste un "change version" et upgrade va juste servir a prendre la derniere release

ENFAITE AVEC --upgrade ou --change apres le pyr4t package install --upgrade


NEW : (d'aboord sortir la release 0.1.0 avec m'ancienne methode)
```
pyr4t
├── init (--app | --cli | --lib) [--authors ...] [--version ...]
├── build
├── deploy [--dev]
├── run [--dev] <script>
├── test
├── fmt
├── cls [--cache] [--log] [--tmp]
├── venv
├── info # info proj actuel
├── install <package-name> [--info] # print les packages dispo avec petite desc et si besoin de token ou non
├── project
│   ├── add <title> <path> <version>
│   ├── list
│   ├── mv <title> [--path ...] [--version ...]
│   ├── rm <title>
│   └── switch <title>
└── user
    ├── add <alias> <name> <email>
    ├── list
    ├── mv <alias> [--email ...] [--name ...]
    ├── rm <alias>
    └── switch <alias>

```

avoir un publish pour publier sur pypi ou github
build nécessite de le pip intsalle ?? mettre en dépendance