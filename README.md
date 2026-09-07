# OthelloX

Lightweight Othello/Reversi engine and UI components in Python.

Overview
--------

OthelloX is a small Python project that implements game logic, an engine, and UI components for the board game Othello (Reversi). It's organized to separate core game mechanics from UI code so you can reuse the engine in different frontends.

Key Features
- Clean game engine and error handling in `othellox.game`
- UI components for boards and cells under `othellox.ui`
- Small, testable modules suitable for experimentation and extension

Project layout
- [src/othellox/app.py](src/othellox/app.py) — application entry point
- [src/othellox/game/board.py](src/othellox/game/board.py) — board model and helpers
- [src/othellox/game/engine.py](src/othellox/game/engine.py) — game engine and rules
- [src/othellox/ui/board/board.py](src/othellox/ui/board/board.py) — UI board component

Requirements
- Python 3.10+ (see `pyproject.toml` for configured metadata)

Installation
```
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

Running

You can run the application module directly:
```bash
python -m othellox.app
```

If you add a UI frontend (CLI, web, or GUI), point it at the engine in `othellox.game`.

Development
- Run linters and formatters you prefer (e.g., `ruff`, `black`).
- Add unit tests under a `tests/` directory and run with `pytest`.

Contributing
- Fork the repo, make small focused changes, and open a PR.
- Describe behavior changes and include tests where applicable.

License
- MIT (or add your preferred license)

Contact
- Open issues on the repository for bugs, feature requests, or questions.

