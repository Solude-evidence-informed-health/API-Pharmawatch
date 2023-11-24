# Pharmawatch-API

O Pharmawatch-API é uma API baseada em FastAPI projetada para lidar com a recuperação e o upload de dados farmacêuticos do Google BigQuery. A API utiliza tokens de usuário para conceder acesso a informações específicas do hospital, permitindo que os usuários recuperem ou façam upload de vários tipos de dados com base em suas permissões.

## Recursos

- **Autenticação Baseada em Token**: Acesso seguro a informações hospitalares e recuperação/upload de dados com base nos tokens do usuário.
- **Recuperação de Dados**: Recupere dados farmacêuticos do BigQuery com base nas permissões do usuário.
- **Upload de Dados**: Faça o upload de diferentes tipos de dados farmacêuticos para o BigQuery por meio de rotas dedicadas.
- **Acesso Específico do Usuário**: Conceda acesso a informações específicas do hospital com base no token do usuário.
- **Versão de Desenvolvimento com Docker**: Experimente facilmente a versão de desenvolvimento da API usando o Dockerfile fornecido.

## Rotas

1. **GET /medicamentos/**
    - Recupere dados farmacêuticos com base nas permissões do usuário.

2. **POST /upload/**
    - Faça upload de vários tipos de dados farmacêuticos para o BigQuery.

3. **GET /info-hospitalar**
    (EM BREVE)
    - Recupere informações detalhadas sobre o hospital associado ao usuário.

4. **GET /info-usuario**
    (EM BREVE)
    - Recupere informações detalhadas sobre o usuário.

5. **GET /medicamentos/filtros**
    - Recupere os filtros disponíveis para a rota de recuperação de dados.

## Utilização para Testes de Desenvolvimento

### Pre-requisitos

- Docker instalado na maquina
- Git instalado na maquina

### Configuração do Ambiente

1. Clone the repository:

    ```bash
    git clone https://github.com/Solude-evidence-informed-health/API-Pharmawatch.git
    cd Pharmawatch-API
    ```

2. Build the Docker image:

    ```bash
    docker build -t pharmawatch-api .
    ```

3. Run the Docker container:

    ```bash
    docker run -p 80:80 pharmawatch-api
    ```

    A API estará acessivel em http://localhost:8000 .

## Executando Testes

Para executar os testes, use o seguinte comando:

```bash
docker exec -it pharmawatch-api python tests/retrieval_test.py
```

## Documentação da API

Acesse a documentação completa da API em http://localhost:8000/docs quando o contêiner Docker estiver em execução.