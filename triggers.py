import time
from config import (
    GAP_CLOSING_THRESHOLD,
    LOW_FUEL_LAPS_THRESHOLD,
    TIRE_TEMP_HIGH,
    TIRE_TEMP_LOW,
    TRIGGER_COOLDOWNS,
)

class TriggerEngine:
    def __init__(self):
        self.last_triggered = {}
        self.previous_best_lap = None

    def _on_cooldown(self, trigger_name):
        last = self.last_triggered.get(trigger_name, 0)
        cooldown = TRIGGER_COOLDOWNS.get(trigger_name, 60)
        return (time.time() - last) < cooldown

    def _mark_triggered(self, trigger_name):
        self.last_triggered[trigger_name] = time.time()

    def check(self, data):
        """Geeft een lijst van (trigger_naam, situatie_beschrijving) terug voor wat nu relevant is."""
        events = []
        if not data:
            return events

        # Laag op brandstof
        fuel_per_lap = data.get("fuel_per_lap")
        fuel_liters = data.get("fuel_liters")
        if (
            fuel_per_lap is not None
            and fuel_per_lap > 0
            and fuel_liters is not None
            and not self._on_cooldown("low_fuel")
        ):
            laps_remaining = fuel_liters / fuel_per_lap
            if laps_remaining < LOW_FUEL_LAPS_THRESHOLD:
                events.append((
                    "low_fuel",
                    f"Fuel is at {laps_remaining:.1f} laps remaining."
                ))
                self._mark_triggered("low_fuel")

        # Gat naar voorligger
        if data.get("gap_ahead") is not None and not self._on_cooldown("gap_closing"):
            if data["gap_ahead"] < GAP_CLOSING_THRESHOLD:
                events.append((
                    "gap_closing",
                    f"Gap to car ahead is closing: {data['gap_ahead']:.3f} seconds."
                ))
                self._mark_triggered("gap_closing")

        # Personal best
        if data.get("best_lap_time") and not self._on_cooldown("personal_best"):
            if self.previous_best_lap and data["best_lap_time"] < self.previous_best_lap:
                events.append((
                    "personal_best",
                    f"New personal best lap time: {data['best_lap_time']:.3f} seconds."
                ))
                self._mark_triggered("personal_best")
            self.previous_best_lap = data["best_lap_time"]

        # Bandentemperatuur
        if not self._on_cooldown("tire_temp_warning"):
            temps = data.get("tire_temps", {})
            hot = [t for t, v in temps.items() if v and v > TIRE_TEMP_HIGH]
            cold = [t for t, v in temps.items() if v and v < TIRE_TEMP_LOW]
            if hot:
                events.append(("tire_temp_warning", f"Tires running hot: {', '.join(hot)}."))
                self._mark_triggered("tire_temp_warning")
            elif cold:
                events.append(("tire_temp_warning", f"Tires running cold: {', '.join(cold)}."))
                self._mark_triggered("tire_temp_warning")

        return events