#!/usr/bin/env python3
"""Exemplo TraCI: conecta no SUMO e conta veículos."""
import os
import sys

if "SUMO_HOME" in os.environ:
    sys.path.append(os.path.join(os.environ["SUMO_HOME"], "tools"))

import traci

sumo_cfg = os.path.join(os.path.dirname(__file__), "..", "simulation.sumocfg")
traci.start(["sumo", "-c", sumo_cfg])

step = 0
try:
    while traci.simulation.getMinExpectedNumber() > 0 and step < 3600:
        traci.simulationStep()
        if step % 300 == 0:
            n = traci.vehicle.getIDCount()
            print(f"step={step} veículos={n}")
        step += 1
finally:
    traci.close()
print("Fim da simulação TraCI.")
