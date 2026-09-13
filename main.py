import time
from config import POLL_INTERVAL, SIMULATOR
from triggers import TriggerEngine
from engineer import get_engineer_response
from voice import Voice


def create_telemetry():
    if SIMULATOR.upper() == "ACC":
        from telemetry_acc import ACCTelemetry

        return ACCTelemetry()

    if SIMULATOR.upper() == "LMU":
        try:
            from telemetry_lmu import LMUTelemetry
        except ModuleNotFoundError as error:
            raise RuntimeError(
                "LMU vereist pyLMUSharedMemory. Clone de library in de "
                "projectmap met: git clone "
                "https://github.com/TinyPedal/pyLMUSharedMemory.git"
            ) from error

        return LMUTelemetry()

    raise ValueError(f"Onbekende simulator: {SIMULATOR!r}. Gebruik ACC of LMU.")


def main():
    telemetry = create_telemetry()
    trigger_engine = TriggerEngine()
    voice = Voice()

    print(f"Race engineer gestart voor {SIMULATOR}. Wachten op telemetrie...")

    try:
        while True:
            data = telemetry.read()
            if data is None:
                time.sleep(POLL_INTERVAL)
                continue

            events = trigger_engine.check(data)
            for _, situation in events:
                response = get_engineer_response(situation)
                if response:
                    voice.say(response)

            time.sleep(POLL_INTERVAL)

    except KeyboardInterrupt:
        print("Gestopt door gebruiker.")
    finally:
        telemetry.close()

if __name__ == "__main__":
    main()