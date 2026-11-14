# POO 2026 - Programação Orientada a Objetos

Repositório dedicado ao armazenamento, prática e evolução dos projetos e exercícios desenvolvidos na disciplina de **Programação Orientada a Objetos (POO)**.

---

## 📁 Estrutura do Repositório

O repositório está organizado nos seguintes módulos e projetos:

```text
poo-2026/
├── PlataformGame/          # Jogo de plataforma 2D em Python (Arcade + Peewee)
│   ├── sprites/            # Folhas de sprites, mapas (.tmx) e tilesets
│   └── src/                # Código-fonte (views, entidades, física, áudio, ranking)
├── InterclassProgram/      # Sistema de gerenciamento de times e interclasse
│   ├── classes.py          # Definições de Player e Team
│   └── main.py             # Interface CLI interativa
├── Peewee Iniciando/       # Prática de banco de dados e ORM Peewee
│   └── Agenda Contato/     # CRUD completo de contatos com SQLite
├── Game/                   # Protótipo inicial de movimentação e janela com Arcade
│   ├── game.py
│   └── shizuka_*.png
├── Exercices/              # Exercícios introdutórios de lógica e estruturas em Python
│   ├── exercice1.py        # Cálculo de médias e aprovação
│   ├── exercice2.py        # Faturamento diário e estatísticas
│   └── exercise3.py        # Simulação de operações bancárias em funções
├── conta_bancaria.py       # Exemplo de modelagem POO (Conta, Depósito, Saque, Transferência)
├── sistema_academico.py    # Exemplo de relacionamentos entre classes (Campus, Estudante, Curso, etc.)
├── aleatorio.py            # Lógica e laços de repetição
├── requirements.txt        # Dependências do repositório
└── .gitignore              # Ignora ambientes virtuais, bancos locais e caches
```

---

## 🚀 Como Executar os Projetos

### 1. Pré-requisitos
- **Python 3.10+** (recomendado Python 3.12)
- Gerenciador de pacotes `pip`

### 2. Criar e ativar o ambiente virtual

No diretório raiz do projeto:

```bash
# Criar ambiente virtual
python3 -m venv .venv

# Ativar ambiente (Linux/macOS)
source .venv/bin/activate

# Ativar ambiente (Windows PowerShell)
# .venv\Scripts\Activate.ps1
```

### 3. Instalar as dependências

```bash
pip install -r requirements.txt
```

---

## 🎮 Executando os Principais Projetos

### PlataformGame
Jogo de plataforma 2D completo desenvolvido com a biblioteca `arcade`, mapas em Tiled (`.tmx`), inimigos com IA, chefão e ranking persistido via Peewee:

```bash
cd PlataformGame/src
python main.py
```

### Agenda de Contatos (Peewee)
Aplicação de console demonstrando operações CRUD (Criar, Listar, Buscar, Editar, Remover) integradas ao banco SQLite:

```bash
cd "Peewee Iniciando/Agenda Contato"
python main.py
```

### InterclassProgram
Gerenciamento de inscrições e formações de equipes para competições escolares:

```bash
cd InterclassProgram
python main.py
```

---

## 🛠️ Tecnologias Utilizadas
- **Python 3**
- **Arcade** (Desenvolvimento de jogos 2D)
- **Peewee ORM** & **SQLite** (Persistência de dados)
- **Tiled** (Construção de mapas em tiles)
