# Flow rate metadata for 175 viruses
# Replace values with real biosensing flow rates if available.

virus_flow_rates_175 = {
    1: 0.015,
    2: 0.018,
    3: 0.020,
    4: 0.022,
    5: 0.025,
    6: 0.028,
    7: 0.030,
    8: 0.033,
    9: 0.035,
    10: 0.038,
    # -------------------------------------------------------
    # You can continue filling real values here.
    # For now, we generate a consistent pattern for all 175.
    # -------------------------------------------------------
}

# Auto-fill remaining virus IDs with a smooth progression
for virus_id in range(1, 176):
    if virus_id not in virus_flow_rates_175:
        virus_flow_rates_175[virus_id] = round(0.015 + virus_id * 0.00015, 5)
