#!/bin/bash
# Gera a rede .net.xml a partir de nodes + edges
set -e
cd "$(dirname "$0")"
netconvert --node-files=networks/nodes.nod.xml \
           --edge-files=networks/edges.edg.xml \
           --output-file=networks/simple.net.xml
echo "Rede gerada: networks/simple.net.xml"
