# AI Race Engineer

## Project Shape

- `main.py` is the runtime entry point. It selects `ACC` or `LMU`, polls telemetry, passes data to `TriggerEngine`, requests an Ollama response, and speaks it through `Voice`.
- `telemetry_acc.py` and `telemetry_lmu.py` are interchangeable adapters. Preserve their shared `read()` -> normalized dictionary and `close()` interface when changing telemetry behavior.
- `triggers.py` owns event detection and per-trigger cooldowns. Thresholds and cooldown values belong in `config.py`, not in the trigger logic.
- `engineer.py` owns the Ollama HTTP request and the radio-engineer system prompt. `voice.py` owns Windows SAPI5 text-to-speech through `pyttsx3`.
- `pyLMUSharedMemory/` is a local third-party shared-memory library. Treat it as an integration boundary and avoid unrelated edits there.

## Runtime Requirements

- This is a Windows-oriented application: `voice.py` uses the SAPI5 `pyttsx3` backend.
- Runtime dependencies are currently implicit in imports (`requests`, `pyttsx3`, `pyaccsharedmemory`, and the local `pyLMUSharedMemory` package). There is no root `requirements.txt`, `pyproject.toml`, or setup script.
- Ollama must be reachable at `config.OLLAMA_HOST` and provide `config.OLLAMA_MODEL` before running the application.
- LMU mode requires the game's shared-memory interface to be available while the game is running. ACC mode requires `pyaccsharedmemory`.
- Change simulator, Ollama settings, polling interval, thresholds, and cooldowns in `config.py` rather than scattering literals through runtime modules.

## Validation

- Run `python -m compileall -q .` after Python changes.
- Run `python pyLMUSharedMemory/tests/read_lmu_api.py` when changing LMU shared-memory structures or adapters and the local LMU dependency is available.
- There is no automated unit-test suite or CI configuration at the repository root. Do not claim runtime behavior is verified unless a simulator and reachable Ollama instance were actually available.

## Coding Conventions

- Keep changes small and consistent with the existing straightforward module structure; avoid introducing a framework or a new abstraction for local fixes.
- Preserve the normalized telemetry keys consumed by `triggers.py` (`fuel_per_lap`, `fuel_liters`, `gap_ahead`, `best_lap_time`, and `tire_temps`).
- Preserve graceful `KeyboardInterrupt` shutdown and telemetry cleanup in `main.py`.
- Existing comments, docstrings, and user-facing diagnostics are largely Dutch, while generated radio responses are intentionally English. Follow the language of the surrounding code.
- Prefer the existing `print()` diagnostics and exception handling style unless a logging change is explicitly requested.