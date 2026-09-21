def physics_estimate(mass_fg, mass_per_virus_fg):
    return mass_fg / mass_per_virus_fg

def simple_ml_time_to_detection(deposition_rate, temperature, humidity, flow_rate):
    base = 20
    return base - 5 * deposition_rate + 0.1 * (humidity - 30) - 0.5 * (flow_rate - 1.5)

def simple_ml_confidence():
    return 0.75
