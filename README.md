# SUMO Projeto

Simulador [Eclipse SUMO](https://eclipse.dev/sumo/) — cruzamento simples.

## Estrutura

```
sumo-projeto/
├── networks/
│   ├── nodes.nod.xml      # nós (cruzamento)
│   ├── edges.edg.xml      # arestas
│   └── simple.net.xml     # gerado pelo netconvert
├── routes/
│   └── routes.rou.xml     # rotas + fluxos
├── scripts/
│   └── run_traci.py       # exemplo TraCI em Python
├── output/                # saídas da simulação
├── simulation.sumocfg     # config principal
├── build.sh               # gera a rede
└── run.sh                 # roda a simulação
```

## 1. Instalar o SUMO (Ubuntu 26.04 / WSL2)

Rode no terminal:

```bash
sudo apt update && sudo apt install -y sumo sumo-tools sumo-doc python3-pip
```

Verifique:

```bash
sumo --version
netconvert --version
sumo-gui --version   # só funciona se tiver display/X11; no WSL2 precisa de WSLg ou X server
echo $SUMO_HOME      # deve ser /usr/share/sumo
```

Se `SUMO_HOME` estiver vazio, adicione ao `~/.bashrc`:

```bash
export SUMO_HOME=/usr/share/sumo
```

## 2. Gerar a rede e rodar

```bash
cd ~/sumo-projeto
chmod +x build.sh run.sh
./build.sh
./run.sh
```

Saída esperada: `Loading configuration... done.` sem erros.

## 3. Com GUI (opcional)

Se tiver tela (Ubuntu desktop ou WSLg):

```bash
sumo-gui -c simulation.sumocfg
```

No WSL2 sem GUI, use o modo texto (`sumo`) mesmo.

## 4. Python / TraCI

```bash
pip3 install -r requirements.txt --break-system-packages
python3 scripts/run_traci.py
```

> No Ubuntu 24.04+, o pip exige `--break-system-packages` ou usar venv:
> `python3 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt`

## Problemas comuns

- `sumo: command not found` → SUMO não instalado. Rode o apt acima.
- `Error: ... simple.net.xml` → rode `./build.sh` primeiro.
- `No module named traci` → `pip3 install traci sumolib` ou defina `SUMO_HOME`.
