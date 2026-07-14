from systems.fuel import calculate_fuel
from systems.tires import check_tires
telemetry = {
    "fuel": 25,
    "fuel_per_lap": 2.4,
    "laps_remaining": 8,

    "tires": {
        "FL": 102,
        "FR": 95,
        "RL": 88,
        "RR": 90
    }
}
print("=== Race Engineer ===")
print(
    calculate_fuel(
        telemetry["fuel"],
        telemetry["fuel_per_lap"],
        telemetry["laps_remaining"]
    )
)
warnings = check_tires(
    telemetry["tires"]
)
for warning in warnings:
    print("⚠", warning)