# AI Race Engineer

Een lokale AI race engineer voor sim racing, die live telemetrie leest uit je sim, betekenisvolle momenten herkent (lage brandstof, snelle sector, bandenproblemen), en daar natuurlijke commentaar over genereert via een lokaal Ollama-model — uitgesproken met tekst-naar-spraak.

Ondersteunt: **Assetto Corsa Competizione (ACC)**, **Le Mans Ultimate (LMU)**, met uitbreidbare structuur voor **Assetto Corsa (AC)**.

## Architectuur

```
[Sim op Windows] → [Python script: telemetrie lezen + trigger-logica]
                          ↓ (HTTP request)
                  [Ollama op lokale server, poort 11434]
                          ↓ (tekstantwoord)
                  [Lokale TTS spreekt het uit]
```

De sim en het script draaien op je Windows gaming-pc. Ollama draait op een aparte (Linux) server in je netwerk en wordt bereikt via HTTP.

## Projectstructuur

```
race-engineer/
├── main.py              # Hoofdloop
├── telemetry_acc.py     # ACC telemetrie-uitlezing
├── telemetry_lmu.py     # LMU telemetrie-uitlezing
├── engineer.py          # Ollama-integratie + prompt-logica
├── voice.py             # Tekst-naar-spraak
├── triggers.py          # Trigger-detectie (wanneer iets zeggen)
├── config.py             # Instellingen
├── chat.py               # Losstaande terminal-chat met de AI (los van de race-functionaliteit)
└── pyLMUSharedMemory/     # Gekloonde library voor LMU-telemetrie (zie Installatie)
```

## Installatie

### Vereisten

- Python 3.10 of hoger
- Git (voor Windows: [git-scm.com/download/win](https://git-scm.com/download/win))
- Een Ollama-server, lokaal of op een andere machine in je netwerk, met een model gedownload (bijv. `llama3.1:8b`)
- ACC en/of Le Mans Ultimate geïnstalleerd

### Stappen

1. Clone of download dit project naar je pc.

2. Maak een virtuele omgeving aan (aanbevolen):
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

3. Installeer de benodigde packages:
   ```bash
   python -m pip install requests pyttsx3 pyaccsharedmemory
   ```

4. Voor LMU-ondersteuning, clone de shared memory library in de project-map:
   ```bash
   git clone https://github.com/TinyPedal/pyLMUSharedMemory.git
   ```

5. Open `config.py` en pas `OLLAMA_HOST` aan naar het IP-adres van je Ollama-server, bijvoorbeeld:
   ```python
   OLLAMA_HOST = "http://192.168.178.60:11434"
   ```

6. Test de verbinding met je Ollama-server:
   ```bash
   curl http://192.168.178.60:11434
   ```
   Krijg je "Ollama is running" terug? Dan is de verbinding goed.

## Gebruik

### Race engineer starten

1. Start je sim (ACC of LMU) en ga de baan op.
2. Kies in `main.py` welke telemetrie-module je gebruikt:
   ```python
   from telemetry_acc import ACCTelemetry   # voor ACC
   # of
   from telemetry_lmu import LMUTelemetry as ACCTelemetry   # voor LMU
   ```
3. Draai het script:
   ```bash
   python main.py
   ```
4. Rij een paar ronden — je zou meldingen moeten horen bij een snelle ronde, lage brandstof, of bandenproblemen.

Stoppen doe je met `Ctrl+C`.

### Losstaande AI-chat (zonder sim)

Wil je gewoon vragen stellen aan je lokale AI, los van de race-functionaliteit:
```bash
python chat.py
```
Typ je vraag, druk Enter, typ `exit` om te stoppen.

## Configuratie aanpassen

Alle instellingen staan in `config.py`:

| Instelling | Beschrijving |
|---|---|
| `OLLAMA_HOST` | Adres van je Ollama-server |
| `OLLAMA_MODEL` | Welk model gebruikt wordt (kleinere modellen = snellere reacties) |
| `POLL_INTERVAL` | Hoe vaak telemetrie gecontroleerd wordt (seconden) |
| `TRIGGER_COOLDOWNS` | Minimale tijd tussen twee meldingen van hetzelfde type |
| `LOW_FUEL_LAPS_THRESHOLD` | Vanaf hoeveel resterende ronden brandstof een waarschuwing komt |
| `GAP_CLOSING_THRESHOLD` | Vanaf welk tijdsverschil een "gat krimpt"-melding komt |
| `TIRE_TEMP_HIGH` / `TIRE_TEMP_LOW` | Temperatuurgrenzen voor bandenwaarschuwingen (Celsius) |

## Bekende beperkingen

- **Geen spotter-functionaliteit.** Dit systeem is niet geschikt voor tijdskritische veiligheidswaarschuwingen (auto's naast je) — daarvoor is een LLM-aanroep te traag. Gebruik hiervoor los CrewChief indien gewenst.
- **LMU: `fuel_per_lap` en `speed_kmh`** worden niet direct door de shared memory library geleverd en zijn nog niet berekend in de huidige versie van `telemetry_lmu.py`.
- **Veldnamen kunnen per sim-versie verschillen.** Als telemetrie niet correct lijkt, controleer de beschikbare velden met:
  ```python
  print(sm.Physics.__dict__)
  print(sm.Graphics.__dict__)
  ```

## Uitbreidingsideeën

- Assetto Corsa (origineel) telemetrie-module toevoegen
- Race-positie en sessietype meenemen in de AI-prompt voor meer context
- Sessies opslaan in een database voor latere analyse
- Spraakherkenning toevoegen om zelf ook vragen te stellen tijdens het rijden
- Meerdere engineer-persoonlijkheden (rustig/kalm vs. fel gedreven)

## Bronnen

- Video-inspiratie: [YouTube](https://www.youtube.com/watch?v=WZC2D38CaVY&t=1074s)
- LMU telemetrie: [pyLMUSharedMemory](https://github.com/TinyPedal/pyLMUSharedMemory)
