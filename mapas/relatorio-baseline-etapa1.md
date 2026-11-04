# Relatório de Andamento — Modelo Baseline
## Otimização de Transporte Público com Q-Learning
**Segue roteiro de: `Definição do Modelo Baseline.pdf`**

---

## 1. Identificação do Projeto

| Item | Descrição |
|------|-----------|
| Nome do projeto | Otimização de Transporte Público com Q-Learning |
| Instituição | UFS — Universidade Federal de Sergipe |
| Disciplina | Fundamentos da Inteligência Artificial |
| Etapa atual | Preparação de mapas + geração da rede SUMO (sem simulação) |
| Data | 16/10/2026 |
| Pasta base | `~/sumo-projeto/` |

## 2. Contexto e Objetivo do Baseline

### 2.1 O que é um baseline?
Modelo de referência determinístico, com regras fixas, que servirá de comparação para provar que o agente de Q-Learning traz ganhos.

### 2.2 Por que precisamos de um baseline?
Sem ele não há como afirmar que a IA melhora tempo de espera, lotação ou uso da frota.

### 2.3 Objetivo deste relatório
Documentar o que **já foi feito** na preparação do cenário que vai suportar o baseline e o Q-Learning sob as mesmas condições e métricas:
frotas 050 | 090 | 091, mapa `.osm` do OpenStreetMap, simulador SUMO, controle TraCI.

> Status: **baseline ainda não implementado em código**. Etapa concluída = mapas importados, redes SUMO geradas e visualizadas (só mapa, sem veículos/rotas).

## 3. Descrição do Cenário Simulado

| Item | Previsto no Baseline | Obtido / Feito |
|------|----------------------|----------------|
| Frotas simuladas | 050 \| 090 \| 091 | PDFs localizados: `050 - CAMPUS_HOSPITAL UNIVERSITARIO.pdf` (849K), `090 - CAMPUS_DIA.pdf` (919K), `091 - CAMPUS_DIA VIA SANTA LUCIA.pdf` (871K) em `Parte 1 (Natália)/` |
| Fonte do mapa | Arquivo `.osm` do OpenStreetMap | 2 arquivos extraídos do zip `Parte 1 (Natália)-20261016T183727Z-1-001.zip` (2.7M): `map.osm` (622K) e `map (1).osm` (969K) |
| Simulador | SUMO | SUMO 1.25.0 confirmado (`sumo --version`, `netconvert --version`), `SUMO_HOME=/usr/share/sumo` |
| Interface de controle | TraCI | Prevista, ainda não usada nesta etapa |

### 3.1 Origem dos mapas (descoberta via tags OSM)

**`map.osm` = Aracaju - Zona Sul**
- `addr:city: Aracaju`, bairros `Distrito Industrial`, `Inácio Barbosa`, `Luzia`
- Vias: `Av. Presidente Tancredo Neves`, `Av. Adélia Franco`, `Av. Empresário José Carlos Silva`
- Bounds: lat -10.95105 a -10.94590, lon -37.07813 a -37.06909
- Centro aprox: -10.9484, -37.0736

**`map (1).osm` = São Cristóvão - Campus UFS**
- `addr:city: São Cristóvão`, bairro `Jardim Rosa Elze`
- Contém: `Universidade Federal de Sergipe`, `Terminal Campus`, `Ginásio da UFS`, `NTI UFS`, `Av. Marechal Rondon`
- Bounds: lat -10.92914 a -10.92069, lon -37.11160 a -37.09620
- Centro aprox: -10.9249, -37.1039

Coerente com as linhas CAMPUS / HOSPITAL UNIVERSITÁRIO que ligam o Campus até Aracaju.

## 4. O Que Foi Feito (passo a passo)

1. **Cópia do zip:**
   `C:\Users\lucas\Downloads\Parte 1 (Natália)-20261016T183727Z-1-001.zip` → `~/sumo-projeto/`
2. **Listagem + extração:**
   `unzip -l` (5 arquivos, 4.3M) + `unzip -o -d ~/sumo-projeto/` → pasta `Parte 1 (Natália)/`
3. **Identificação da região** por parsing XML das tags `addr:city`, `addr:suburb`, `name`, `amenity=university`.
4. **Geração das redes SUMO com `netconvert`** (só mapa, sem rotas):
   - `networks/aracaju.net.xml` a partir de `map.osm`
   - `networks/ufs-campus.net.xml` a partir de `map (1).osm`
   - Flags: `--geometry.remove --roundabouts.guess --ramps.guess --junctions.join --tls.guess-signals --tls.discard-simple --tls.join`
5. **Visualização sem simulação:**
   - plots `aracaju.png` (234K) e `ufs-campus.png` (202K) via `sumolib.net.readNet + matplotlib`
   - configs só-rede `view-aracaju.sumocfg` e `view-ufs-campus.sumocfg` (sem `<route-files>`) para abrir no `sumo-gui`
6. **Organização:**
   - pasta `mapas/` + `mapas/comandos-mapas.txt` com todos os comandos usados.

Comandos completos em: `mapas/comandos-mapas.txt`

## 5. Redes Geradas — Resultado

| Rede | Origem | Arquivo | Edges | Comprimento total | Nodes | Área |
|------|--------|---------|-------|-------------------|-------|------|
| Aracaju | `map.osm` | `networks/aracaju.net.xml` (1.1M) | 524 (456x1 faixa, 16x2, 46x3, 6x4+) | 37.7 km | 260 | 4.03 km² |
| UFS Campus | `map (1).osm` | `networks/ufs-campus.net.xml` (2.4M) | 1322 (1267x1 faixa, 54x2, 1x3) | 85.89 km | 612 | 10.42 km² |

Estatísticas via `tools/net/network_statistics.py -n`.

Visual:
- Aracaju: eixo diagonal Tancredo Neves + malha do Distrito Industrial, trevo central bem visível.
- UFS Campus: retângulo do campus no centro-direita, bairro Rosa Elze quadriculado à esquerda, eixo Marechal Rondon e saída para Aracaju embaixo-esquerda.

> Nenhum veículo, rota ou semáforo atuado foi simulado nesta etapa, conforme solicitado ("somente o mapa").

## 6. Regras do Baseline (previstas — ainda não codificadas)

Conforme `Definição do Modelo Baseline.pdf`, a implementar sobre as redes acima:

- **4.1 Despacho:** partida a cada T fixo. `HEADWAY = 10 min`. Sai vazio se sem fila; sai lotado se com fila.
- **4.2 Parada:** para em todos os pontos, exceto se `LOTACAO_MAX = 90%` → pula ponto.
- **4.3 Frota:** fixa. `FROTA_FIXA = 5 (doc §4.3) / 6 (tabela §5)` — definir 1 valor antes de codar.
- **4.4 Embarque:** `FIFO`.
- **4.5 Priorização:** nenhuma.

Tabela resumo alvo:

| Parâmetro | Valor | Unidade |
|-----------|-------|---------|
| Headway fixo | 10 | min |
| Limite lotação | 90 | % |
| Frota | 5 ou 6 (a definir) | ônibus |
| Embarque | FIFO | — |
| Tempo simulação | 4 | horas (pico manhã) |
| Pular ponto se lotado | Sim | — |

## 7. Métricas de Comparação (a coletar nas próximas etapas)

| Métrica | Descrição | Unidade | Meta Q-Learning |
|---------|-----------|---------|-----------------|
| Tempo médio de espera | média na fila | min | Reduzir X% vs baseline |
| Lotação média | ocupação média | % | Manter <90% |
| Viagens realizadas | total no período | un | [definir] |
| Passageiros atendidos | total embarcados | un | [definir] |
| Variância espera | consistência | min² | Reduzir |

Nada medido ainda — redes sem demanda não geram métricas.

## 8. Justificativa do Baseline (mantida)
- Baseado em operação real urbana.
- Determinístico e reproduzível, sem aprendizado.
- Representa operação tradicional sem IA.

## 9. Limitações Atuais
As do documento + as desta etapa:
- Não se adapta a picos; cego a distribuição espacial; frota não otimizada; risco de ônibus vazio / fila longa.
- **Etapa atual:** sem demanda (sem `rou.xml`, sem pontos de ônibus mapeados para as linhas 050/090/091), sem calibração com PDFs de itinerário, duas redes separadas (falta conector Campus↔Aracaju para simular linha completa), sem TraCI/Q-Learning.

## 10. Próximos Passos
1. Definir FROTA (5 ou 6) e congelar parâmetros §5.
2. Extrair itinerários dos 3 PDFs e mapear pontos/paradas nas 2 redes.
3. Gerar demanda + `routes.rou.xml` (4h pico manhã) e `simulation.sumocfg` com baseline (pseudocódigo §6 do doc).
4. Rodar baseline, coletar métricas §7.
5. Implementar agente Q-Learning / Deep Q-Learning (ver discussão: DQN é para **controle**, não para **simular**; avaliar PPO/A2C para semáforo/despacho) via TraCI nas mesmas condições.
6. Comparar baseline x Q-Learning.

## 11. Referências
- Documentação SUMO — TraCI: https://sumo.dlr.de/docs/TraCI.html
- OpenStreetMap: https://www.openstreetmap.org/
- Arquivos: `Parte 1 (Natália)/map.osm`, `Parte 1 (Natália)/map (1).osm`, `networks/aracaju.net.xml`, `networks/ufs-campus.net.xml`, `aracaju.png`, `ufs-campus.png`

## Anexo — Onde está cada coisa
```
sumo-projeto/
  Parte 1 (Natália)-20261016T183727Z-1-001.zip
  Parte 1 (Natália)/ 050...pdf, 090...pdf, 091...pdf, map.osm, map (1).osm
  networks/aracaju.net.xml
  networks/ufs-campus.net.xml
  aracaju.png / ufs-campus.png
  view-aracaju.sumocfg / view-ufs-campus.sumocfg
  mapas/comandos-mapas.txt
```
