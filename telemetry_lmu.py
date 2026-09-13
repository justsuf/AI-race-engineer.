"""Optionele LMU-telemetrieadapter.

Vereist een lokale clone van pyLMUSharedMemory in de projectmap.
"""

import math

from pyLMUSharedMemory.lmu_data import SimInfo


class LMUTelemetry:
    def __init__(self):
        self.sim_info = SimInfo()
        self.previous_lap = None
        self.previous_fuel = None
        self.fuel_per_lap = None

    def read(self):
        """Lees LMU-telemetrie in hetzelfde formaat als de ACC-adapter."""
        data = self.sim_info.LMUData
        telemetry = data.telemetry
        scoring = data.scoring

        player_idx = telemetry.playerVehicleIdx
        if not telemetry.playerHasVehicle or player_idx >= telemetry.activeVehicles:
            return None

        player_telem = telemetry.telemInfo[player_idx]
        player_scoring = scoring.vehScoringInfo[player_idx]

        completed_laps = player_scoring.mTotalLaps
        fuel_per_lap = self._estimate_fuel_per_lap(
            completed_laps, player_telem.mFuel
        )

        def avg_temp_celsius(wheel):
            return sum(wheel.mTemperature) / 3 - 273.15

        return {
            "speed_kmh": math.hypot(
                player_telem.mLocalVel.x, player_telem.mLocalVel.z
            ) * 3.6,
            "fuel_liters": player_telem.mFuel,
            "fuel_capacity": player_telem.mFuelCapacity,
            "fuel_per_lap": fuel_per_lap,
            "current_lap_time": player_scoring.mCurSector2,
            "best_lap_time": player_scoring.mBestLapTime,
            "last_lap_time": player_scoring.mLastLapTime,
            "position": player_scoring.mPlace,
            "tire_temps": {
                "FL": avg_temp_celsius(player_telem.mWheels[0]),
                "FR": avg_temp_celsius(player_telem.mWheels[1]),
                "RL": avg_temp_celsius(player_telem.mWheels[2]),
                "RR": avg_temp_celsius(player_telem.mWheels[3]),
            },
            "gap_ahead": player_scoring.mTimeBehindNext,
            "completed_laps": completed_laps,
            "in_pits": player_scoring.mInPits,
        }

    def _estimate_fuel_per_lap(self, completed_laps, fuel):
        if self.previous_lap is not None and completed_laps > self.previous_lap:
            fuel_used = self.previous_fuel - fuel
            if fuel_used > 0:
                self.fuel_per_lap = fuel_used / (completed_laps - self.previous_lap)

        self.previous_lap = completed_laps
        self.previous_fuel = fuel
        return self.fuel_per_lap

    def close(self):
        self.sim_info.close()