
# Techlab DevOps Challenge

Bem vindo ao repoitório de código do desafio Devops Techlab!

## Objetivo da aplicação

Com esse projeto, visa-se criar uma script ETL para transformar e gerar informações sobre os custos de uma empresa com seus funcionários, levando em consideração todos os beneficios concedidos a estes.

Documento de requisitos: [Desafio techlab](https://link-da-documentação)
## Documentação

### Menu de opções iniciais

### Funcionamento

### Arquitetura

### Hierarquia de comunicação

### Prompts

### Tempo de execução
## Como rodar

Requisitos:

Clone o projeto

```bash
  git clone https://
  cd DevOps-challenge
```

Crie e ative um ambiente virtual Python

```bash
  python -m venv venv
  source venv/bin/activate
```

Instale as bibliotecas do projeto

```bash
  pip install -r requirements.txt
```

    
Copie o arquivo .env e preencha sua GROQ_API_KEY

```bash
  cp .env.exemple .env
```

[Join Groq Here](https://link-da-documentação)


Rode o projeto

```bash
  python main.py
```

O menu demontrado aparecerá no terminal.



## Explicações e Preferências técnicas

### Modelos LLM usados

Para a análise de cada arquivo de entrada, foi utilizado o modelo XXXX, pois este, dentre os disponíveis, era o mais adequado para análise de dados e percepção de padrões para melhorias e limpeza dos dados.
Já para a manipulação e transformação dos dados, assim como geração e aplicação das regras de rateio, foi utilizado o YYYY, pois possui capacidade de manejar grande volumes de dados com facilidade.

### Por que essa arquitetura?

Inicialmente, devido ao escopo reduzido do projeto, optei por não utilizar nenhum framework inicializador, mas sim criar manualmente a arquitetura conforme necessidades e seguindo padrões já sabidos.
Assim, devido as condições, não foi identificada a necessidade de algo mais complexo.

## Tendências Futuras

- Uso de agents que suportem upload de arquivos: Visando maior precisão e escalabilidade.
- Integração com banco de dados: O projeto se limita ao uso de fontes .xlsx, o que demanda manutenção e troca manual periódica desses dados. Uma conexão sólida com um banco de dados volumoso pode ser benéfica para análise de mais indicadores.
- Interface melhorada: A medida em que cresce a necessidade e a quantidade de dados, uma interface web se faz necessária para melhor visualização dos dados. 
- Novas funcionalidades: As tranformações possíveis durante o fluxo foram restringidas devido ao escopo reduzido do projeto, mas novas e mais específicas operações podem ser adicionadas (Como pivot ou unpivot, por exemplo).
- Fluxo melhorado: Dependendo do foco, se for necessário maior precisão dos dados ou maior rapidez na geração, pode-se aumentar ou diminuir o número de chamadas a agent, assim como variar os modelos para mais específicos/melhores.
## Autores

- [@erick-bonifacio](https://www.github.com/erick-bonifacio)
