#!/bin/bash
# Roda a simulação (modo texto). Use sumo-gui se tiver display.
set -e
cd "$(dirname "$0")"
if [ ! -f networks/simple.net.xml ]; then
  echo "Rede não encontrada, gerando..."
  ./build.sh
fi
sumo -c simulation.sumocfg
