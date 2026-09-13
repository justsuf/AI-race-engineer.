from pyaccsharedmemory import accSharedMemory


class ACCTelemetry:
    def __init__(self):
        self.asm = accSharedMemory()

    def read(self):
        """Leest de huidige telemetrie-snapshot en geeft een simpel dict terug."""
        sm = self.asm.read_shared_memory()
        if sm is None:
            return None

        return {
            "speed_kmh": sm.Physics.speed_kmh,
            "fuel_liters": sm.Physics.fuel,
            "fuel_per_lap": self._estimate_fuel_per_lap(sm),
            "current_lap_time": sm.Graphics.current_time,
            "best_lap_time": sm.Graphics.best_time,
            "last_lap_time": sm.Graphics.last_time,
            "position": sm.Graphics.position,
            "tire_temps": {
                "FL": sm.Physics.tyre_core_temp.front_left,
                "FR": sm.Physics.tyre_core_temp.front_right,
                "RL": sm.Physics.tyre_core_temp.rear_left,
                "RR": sm.Physics.tyre_core_temp.rear_right,
            },
            "gap_ahead": sm.Graphics.delta_lap_time,
            "completed_laps": sm.Graphics.completed_lap,
        }

    def _estimate_fuel_per_lap(self, sm):
        return getattr(sm.Graphics, "fuel_per_lap", None)

    def close(self):
        self.asm.close()