# Projeto Django com Monitoramento XML

Este projeto é uma aplicação Django que monitora uma pasta em busca de arquivos XML, processa esses arquivos e armazena os dados em um banco de dados PostgreSQL. Os dados podem ser visualizados através de uma interface web React.

## Estrutura do Projeto

```
ProjetoDjango/
├── backend/              # Aplicação Django
│   ├── api/              # API REST para acesso aos dados
│   ├── dados_importados/ # Modelos e views para dados importados
│   ├── meu_projeto/       # Configurações do projeto Django
│   ├── watchdog_monitoramento/ # Script de monitoramento de arquivos XML
│   └── manage.py         # Script de gerenciamento do Django
├── frontend/             # Aplicação React para interface web
└── README.md             # Este arquivo
```

## Funcionalidades

### 1. Monitoramento de Arquivos XML
O script em `backend/watchdog_monitoramento/watch_xml.py` monitora continuamente a pasta `pastaMonitorada` em busca de novos arquivos XML. Quando um arquivo é detectado:

1. Aguarda a estabilização do arquivo (para garantir que o arquivo foi completamente escrito)
2. Lê e parseia o conteúdo XML
3. Extrai os dados e os armazena no banco de dados

### 2. API REST
A API REST em `backend/api/` fornece endpoints para acessar os dados importados:

- `GET /api/desembaraco/` - Retorna todos os dados importados

### 3. Interface Web
A interface web em `frontend/` exibe os dados importados em uma tabela interativa.

## Modelos de Dados

Os dados importados são organizados em modelos relacionados para melhor manutenção:

- `DadosImportados` - Modelo principal
- `DocumentInfo` - Informações sobre documentos
- `StatusInfo` - Informações sobre status
- `DateInfo` - Informações sobre datas
- `DeliveryInfo` - Informações sobre entrega
- `DelayInfo` - Informações sobre atrasos
- `FundInfo` - Informações sobre fundos

## Como Usar

### Configuração do Ambiente

1. Instale as dependências do backend:
```bash
cd backend
pip install -r requirements.txt
```

2. Configure as variáveis de ambiente criando um arquivo `.env` na pasta `backend/`:
```
SECRET_KEY=sua_secret_key_aqui
DB_NAME=nome_do_banco
DB_USER=usuario_do_banco
DB_PASSWORD=senha_do_banco
DB_HOST=localhost
DB_PORT=5432
```

3. Execute as migrações do banco de dados:
```bash
python manage.py migrate
```

4. Instale as dependências do frontend:
```bash
cd frontend
npm install
```

### Executando o Projeto

1. Inicie o servidor Django:
```bash
cd backend
python manage.py runserver
```

2. Inicie o script de monitoramento (em um terminal separado):
```bash
cd backend/watchdog_monitoramento
python watch_xml.py
```

3. Inicie o servidor de desenvolvimento React (em um terminal separado):
```bash
cd frontend
npm start
```

## Endpoints da API

- `http://localhost:8000/api/desembaraco/` - Lista todos os dados importados

## Estrutura dos Arquivos XML

O script espera arquivos XML com a seguinte estrutura:

```xml
<root>
  <NewReportItem>
    <ref_giant>valor</ref_giant>
    <mawb>valor</mawb>
    <!-- outros campos -->
  </NewReportItem>
  <!-- mais itens -->
</root>