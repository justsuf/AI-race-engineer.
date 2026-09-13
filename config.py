# Ollama server instellingen
OLLAMA_HOST = "http://192.168.178.60:11434"
OLLAMA_MODEL = "llama3.1:8b"

# Actieve simulator: "ACC" of "LMU"
SIMULATOR = "LMU"

# Hoe vaak telemetrie gecontroleerd wordt (seconden)
POLL_INTERVAL = 1.0

# Cooldown per trigger-type, voorkomt spam (seconden)
TRIGGER_COOLDOWNS = {
    "low_fuel": 120,
    "personal_best": 30,
    "gap_closing": 20,
    "tire_temp_warning": 90,
}

# Drempelwaarden
LOW_FUEL_LAPS_THRESHOLD = 5
GAP_CLOSING_THRESHOLD = 0.5
TIRE_TEMP_HIGH = 110
TIRE_TEMP_LOW = 60