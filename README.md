# Sistema de Tickets do Discord

Este repositório contém o código para um bot de suporte para servidores Discord. O bot gerencia e organiza tickets de suporte de uma maneira eficiente e automatizada. Ele usa uma estrutura de dados no Redis para manter o estado dos tickets, facilitando assim um ambiente de suporte ágil e responsivo.

## Principais Funcionalidades

- **Criação de Tickets:** O bot permite que os usuários criem tickets de suporte escolhendo uma categoria em um menu suspenso.

- **Exclusão de Tickets:** Os tickets podem ser excluídos com um botão de excluir. Isso aciona um prompt de confirmação para evitar a exclusão acidental de tickets.

- **Persistência de Dados:** O bot usa um banco de dados Redis para armazenar os estados dos tickets, o que permite que o bot seja reiniciado sem perder o controle dos tickets abertos.

## Colaboração

Contribuições para o projeto são bem-vindas. Se desejar contribuir, faça um fork do repositório, faça suas alterações e inicie uma solicitação de pull. Certifique-se de aderir aos padrões de codificação já estabelecidos dentro do projeto e descreva claramente as alterações feitas ao enviar sua solicitação de pull.

Este bot é um projeto em andamento. Como tal, existem muitos aprimoramentos e funcionalidades ainda a serem implementados. Sinta-se à vontade para explorar os problemas, participar de discussões ou propor novos recursos.

Leia o guia [README](README.md) para mais informações.

## Licença

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE.md) para detalhes.

## Como Configurar o Redis

### Linux

1. Atualize os pacotes do sistema:

```bash
sudo apt update
```

2. Instale o Redis:

```bash
sudo apt install redis-server
```

3. Abra o arquivo de configuração do Redis:

```bash
sudo nano /etc/redis/redis.conf
```

4. Encontre a linha que contém `supervised no` e altere para `supervised systemd`.

5. Salve o arquivo e feche o editor.

6. Reinicie o serviço Redis:

```bash
sudo systemctl restart redis.service
```

### Windows

1. Baixe a versão mais recente do Redis para Windows [aqui](https://github.com/microsoftarchive/redis/releases).

2. Descompacte o arquivo e execute `redis-server.exe`.

### macOS

1. Instale o Homebrew, caso ainda não o tenha feito:

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

2. Instale o Redis:

```bash
brew install redis
```

3. Inicie o serviço Redis:

```bash
brew services start redis
```

Para mais detalhes, consulte a documentação oficial do Redis.