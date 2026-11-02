#  Local Task Manager

Aplicación de línea de comandos (CLI) para gestionar tareas pendientes, escrita en **Python puro** y con guardado local en JSON. Sin dependencias externas.

![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey)
![License](https://img.shields.io/badge/license-MIT-green)

---

##  Características

-  Menú interactivo **y** comandos escritos en una sola línea
-  Añadir, listar, completar, reabrir y borrar tareas
-  Guardado automático en `tasks.json` (junto al script)
-  Solo librería estándar de Python — cero dependencias
-  Portable: copia la carpeta a cualquier sitio y sigue funcionando
-  Funciona en Windows, macOS y Linux

##  Requisitos

- Python **3.8** o superior
- Una terminal (Windows Terminal, PowerShell, cmd, VS Code integrada…)

##  Instalación

```bash
git clone https://github.com/TU-USUARIO/local-task-manager.git
cd local-task-manager
```

No hay nada que instalar. Con tener Python, funciona.

Alternativamente, descarga el ZIP desde el botón **Code → Download ZIP** y descomprímelo.

##  Uso

```bash
python Todo.py
```

Se mostrará el menú y el prompt `todo>`. Puedes escribir un número del menú o un comando completo:

```
====================================
         LOCAL TASK MANAGER
====================================
  add / 1           Add a new item
  list / 2          Show the list
  done / 3          Mark item as completed
  undo / 4          Mark item as not done
  delete / 5        Delete an item
  menu / ?          Show this menu
  exit / 0          Quit

====================================
todo> add Buy milk
+ Added #1: Buy milk

todo> add Call mom
+ Added #2: Call mom

todo> list

  [ ]   1  Buy milk
  [ ]   2  Call mom

  0/2 completed

todo> done 1
* Completed #1: Buy milk

todo> 2

  [x]   1  Buy milk
  [ ]   2  Call mom

  1/2 completed

todo> delete 2
Delete #2 'Call mom'? [y/N] y
- Deleted #2: Call mom

todo> exit
Bye!
```

### Comandos

| Comando                    | Alias                    | Menú | Descripción                           |
| -------------------------- | ------------------------ | :--: | ------------------------------------- |
| `add <texto>`              | `add`                    | `1`  | Añade una tarea. Sin texto, la pide.  |
| `list`                     |                          | `2`  | Muestra todas las tareas              |
| `done <id>`                | `d`, `complete`          | `3`  | Marca la tarea como completada        |
| `undo <id>`                | `u`, `reopen`            | `4`  | Marca la tarea como pendiente         |
| `delete <id>`              | `del`, `rm`, `remove`    | `5`  | Borra la tarea (pide confirmación)    |
| `menu`                     | `m`, `?`                 |      | Muestra la ayuda                      |
| `exit`                     | `quit`, `q`              | `0`  | Sale del programa                     |

> El `<id>` de `done`, `undo` y `delete` es **opcional**. Si lo omites, el programa te muestra la lista y te pregunta qué tarea.

### Trucos

- Las comillas se aceptan y se eliminan: `add "Buy milk"` es igual que `add Buy milk`.
- Cierra con `Ctrl+C` en cualquier momento — se guarda antes de salir.

##  Dónde se guardan los datos

Junto al script, en `tasks.json`:

```json
[
  {
    "id": 1,
    "title": "Buy milk",
    "completed": true,
    "created": "2026-11-02T14:32:10"
  }
]
```

Es un JSON legible y editable a mano. **No lo subas al repo**: ya está en `.gitignore`.

##  Estructura del proyecto

```
local-task-manager/
├── Todo.py        # la aplicación
├── README.md
├── LICENSE
└── .gitignore     # (tasks.json no se versiona)
```

##  Contribuir

Ideas, pull requests y sugerencias son bienvenidas. Abre un **issue** con lo que se te ocurra.

Ideas para futuros añadidos:
- Filtros `list --pending` / `list --done`
- Fechas límite (`add "..." --due 2026-12-01`)
- Prioridades
- Búsqueda (`search <palabra>`)
- Backend SQLite (sigue sin dependencias con `sqlite3` de la stdlib)

##  Licencia

[MIT](LICENSE)