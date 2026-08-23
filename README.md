# Gil Vicente FC — Desafio Data Scientist

Análise de dados de evento IMPECT (8 jogos, época 2025/26) para identificar
insights táticos relevantes para uma equipa técnica que se prepara para
defrontar o Gil Vicente FC.

## Estrutura do repositório

```
├── NotebookGilVicente.ipynb     # notebook com toda a análise, código e visualizações
├── DashboardGilVicente.py       # dashboard interativo (Streamlit), complementar ao notebook
├── apresentacao/                # apresentação final (5 slides)
├── .gitignore                   # exclui os dados IMPECT do repositório
└── README.md
```

## Abordagem

O trabalho seguiu um processo de exploração aberta: testei várias hipóteses
de fraqueza/força ofensiva e defensiva do Gil Vicente, validando sempre
cada padrão encontrado contra os 8 adversários da amostra antes de o dar
como distintivo (várias hipóteses iniciais foram testadas e descartadas por
não se distinguirem da média dos adversários — esse percurso está
documentado no próprio notebook, na secção do insight 2). Os dois insights
finais sobreviveram a essa validação e foram ainda reforçados com um modelo
estatístico (regressão logística) para o insight 1.

## Como correr localmente

### Requisitos

```bash
pip install pandas numpy matplotlib mplsoccer statsmodels streamlit plotly
```

### Dados

Os dados IMPECT (8 ficheiros `.pkl`, um por jogo) **não estão incluídos**
neste repositório — ver `.gitignore` e nota abaixo. Coloca os ficheiros
numa pasta local e ajusta a variável `PASTA_DADOS` (no início do notebook
e do dashboard) para o caminho dessa pasta.

### Notebook (análise principal)

```bash
jupyter notebook NotebookGilVicente.ipynb
```

### Dashboard interativo (opcional, complementar)

```bash
streamlit run DashboardGilVicente.py
```

## Resumo dos insights

**Insight 1 — Lançamento lateral como arma ofensiva**
50% dos golos do Gil Vicente nesta amostra (4 de 8) vieram de lançamento
lateral — mais do que cantos e livres combinados, apesar de muito menos
volume de eventos. O lançador Santi García converte 31% dos seus
lançamentos em remate (vs. 3.4% do lançador mais utilizado), efeito
validado por regressão logística (odds ratio 8.7, p<0.001) mesmo
controlando pela distância do lançamento — é a qualidade da entrega, não o
alcance.

**Insight 2 — Contenção de cruzamentos**
O Gil Vicente contém 84.3% dos cruzamentos sofridos, +7.4pp acima da média
dos 8 adversários. Mas essa força concentra-se no cruzamento alto — no
cruzamento rasteiro, sobretudo vindo do flanco esquerdo e de zona mais
recuada da linha de fundo, o Gil Vicente fica abaixo da média.

Metodologia completa, evidência quantitativa, interpretação futebolística,
aplicação prática e limitações de cada insight estão documentadas no
notebook.

## Nota sobre os dados

Os dados de evento IMPECT usados nesta análise não são publicados,
incluídos ou partilhados com terceiros neste repositório, por instrução do
enunciado do desafio.

---
Trabalho realizado por: Ricardo Bonança
