# ConfiMusic

Este é um projeto de exemplo que utiliza o [Flask](https://flask.palletsprojects.com/en/2.2.x/) para criar uma API que permite a listagem das 10 músicas mais ouvidas de um artista.

## Configuração do Ambiente

Para configurar o ambiente, você deve seguir os seguintes passos:

1. Certifique-se de ter o Python 3.9 instalado em sua máquina.
2. Crie um ambiente virtual com o seguinte comando:

    ```
    python -m venv venv
    ```

3. Ative o ambiente virtual:

    ```
    >Linux
    source venv/bin/activate
    >Windows
    .\venv\Scripts\activate 
    ```

4. Instale as dependências do projeto com o seguinte comando:

    ```
    pip install -r requirements.txt
    ```

5. Crie um arquivo `.env`, na pasta raiz do projeto, com as seguintes variáveis de ambiente:

    ```
    REDIS_HOST="Host do Redis"
    REDIS_PORT="Sua porta do Redis"
    REDIS_PASSWORD="Senha do Redis(SE HOUVER)"
    GENIUS_API_TOKEN="Genius access token"
    DYNAMODB_REGION="Região que a tabela do DynamoDB foi criada"
    DYNAMODB_TABLE_NAME="Nome da tabela no DynamoDB"
    ```

## Configuração do Redis

### Configurando o Redis sem Docker (apenas macOS/Linux)

1. Baixe o Redis do site oficial [aqui](https://redis.io/download).
2. Extraia o arquivo baixado usando o comando tar xzf redis-VERSION.tar.gz, onde VERSION é a versão que você baixou.
3. Navegue até o diretório extraído usando o comando cd redis-VERSION.
4. Compile o Redis executando o comando make.
5. Instale o Redis executando o comando make install.
6. O Redis estará instalado no sistema operacional. Verifique novamente a instalação executando o comando redis-cli -v.
7. Para iniciar o servidor Redis, execute o comando redis-server no terminal.
8. O Redis deve estar rodando em segundo plano. Para verificar, execute o comando redis-cli ping. Você deve receber uma resposta PONG.

### Configurando o Redis com Docker (Windows + macOS/Linux)

Certifique-se de que o Docker está instalado na sua máquina. Você pode fazer o download do Docker [aqui](https://www.docker.com/products/docker-desktop/).

Abra o terminal e execute o seguinte comando para baixar a imagem do Redis:

 ```
docker pull redis
 ```

Após a imagem ser baixada, execute o seguinte comando para criar um novo contêiner do Redis:

 ```
docker run --name redis-instance -p 6379:6379 -d redis
 ```

O comando acima cria um contêiner do Redis com o nome "redis-instance", expõe a porta 6379 do contêiner para a porta 6379 da máquina local e executa o contêiner em segundo plano.

Verifique se o contêiner está sendo executado usando o seguinte comando:

 ```
docker ps
 ```

Você deverá ver o contêiner do Redis sendo executado na lista de contêineres.

Agora, você pode usar um cliente Redis como Redis Desktop Manager ou o próprio cliente Redis do terminal.

 ```
redis-cli
 ```

O comando acima inicia o cliente Redis do terminal.

## Configuração das Credenciais da AWS

    AWS_ACCESS_KEY_ID = a chave de acesso da sua conta da AWS
    AWS_SECRET_ACCESS_KEY = a chave secreta da sua conta da AWS
    AWS_DEFAULT_REGION: a região padrão que você deseja usar
Você pode definir essas variáveis de ambiente de diferentes maneiras, dependendo do seu sistema operacional e preferências pessoais. Aqui estão algumas maneiras de fazer isso:

### No Linux e macOS

```bash
export AWS_ACCESS_KEY_ID=YOUR_ACCESS_KEY_ID
export AWS_SECRET_ACCESS_KEY=YOUR_SECRET_ACCESS_KEY
export AWS_DEFAULT_REGION=YOUR_REGION
 ```

### No Windows

```powershell
setx AWS_ACCESS_KEY_ID "YOUR_ACCESS_KEY_ID"
setx AWS_SECRET_ACCESS_KEY "YOUR_SECRET_ACCESS_KEY"
setx AWS_DEFAULT_REGION "YOUR_REGION"
 ```

### Caso nenhuma opção acima funcione

 Para adicionar suas credenciais da AWS no arquivo ~/.aws/credentials você pode seguir os seguintes passos

1. Na pasta raiz do seu usuário crie a pasta '.aws' com o arquivo 'credentials' dentro:

2. Adicione suas credenciais da AWS no arquivo 'credentials', utilizando a seguinte sintaxe:

    ```credentials
    [default]
    aws_access_key_id = SUA_ACCESS_KEY_AQUI
    aws_secret_access_key = SUA_SECRET_KEY_AQUI
    aws_default_region = SUA_REGIAO_AQUI
    ```

3. Substitua SUA_ACCESS_KEY_AQUI, SUA_SECRET_KEY_AQUI e SUA_REGIAO_AQUI pelas suas respectivas informações de credenciais da AWS.

4. Salve e feche o arquivo.

5. Se quiser verificar se suas credenciais foram adicionadas corretamente, digite o seguinte comando no terminal:

    ```prompt
    >Linux
    cat ~/.aws/credentials
    >Windows
    type credentials
    ```

Isso irá exibir as informações do arquivo credentials, incluindo suas credenciais da AWS.

 Certifique-se de substituir YOUR_ACCESS_KEY_ID, YOUR_SECRET_ACCESS_KEY e YOUR_REGION pelas suas próprias credenciais e região da AWS.

## Configuração da tabela no DynamoDB

Para criar a tabela usada nesse projeto no seu DynamoDB execute o seguinte comando:

```
python utils/criar_tabela.py
```

## Teste Unitário

Para executar o teste unitário executer o seguinte comando na raiz do projeto:

```
python test_unitario.py
```

## Docker

Para rodar essa API em um container no Docker siga esses passos:

1. Na pasta raiz do projeto execute esse comando para construi a imagem no Docker:

    ```cmd
    docker build --no-cache -t confimusic .    
    ```

2. Após construir a imagem você deve ser atentar a uma coisa, o arquivo '.env' na raiz do projeto possui os dados do projeto executado em python, para executar o projeto no Docker é necessário configurar um arquivo .env separado do principal, dentro de alguma pasta no projeto sem ser a pasta raiz.
3. Após criar esse arquivo views/.env.docker, por exemplo, é necessário preencher com dados parecidos com o arquivo .env mas com algumas alterações para funcionar no Docker, exemplo:

    ```.env.docker
    REDIS_HOST=HOST DA SUA IMAGEM DO DOCKER
    >Para obter o host da imagem do Docker execute'docker ps' no terminal, procure o id da imagem do redis  'docker inspect id_da_imagem' e procure pelo campo: "IPAddress" e copie e cole no REDIS_HOST
    REDIS_PORT=PORTA QUE O CONTAINER ESTÁ SENDO EXECUTADA
    #REDIS_PASSWORD= AQUI SE SEU CONTAINER PRECISA É SÓ REMOVER O # DE COMENTÁRIO E DIGITAR A SENHA
    GENIUS_API_TOKEN=ACCESS TOKEN DA API DO GENIUS
    DYNAMODB_REGION=REGIÃO QUE FOI CRIADA A TABELA NO DYNAMODB
    DYNAMODB_TABLE_NAME=NOME DA TABELA CRIADA NO DYNAMODB
    ```

4. Após a configuração das variáveis de ambiente do Docker execute esse comando, para rodar a imagem:

    ```cmd
    docker run --env-file=views/<arquivo_env_criado_para_o_docker> -p 5000:5000 confimusic
    > exemplo: docker run --env-file=views/.env.docker -p 5000:5000 confimusic
    ```

## Executando a API

Para executar a API, você pode rodar o seguinte comando na raiz do projeto:

```
python app.py
```
