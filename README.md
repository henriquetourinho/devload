# DevLoad — A Rede Social para Desenvolvedores

<p align="left">
    <img src="https://img.shields.io/badge/versão-v1.0-blue.svg" alt="Versão">
    <img src="https://img.shields.io/badge/licença-GPL_v3-blue.svg" alt="Licença">
    <img src="https://img.shields.io/badge/Python-3.8%2B-cyan.svg" alt="Python Version">
    <img src="https://img.shields.io/badge/UI-Tkinter-orange.svg" alt="UI Framework">
    <img src="https://img.shields.io/badge/Banco_de_Dados-MySQL-blue.svg" alt="Banco de Dados">
    <img src="https://img.shields.io/badge/feito_no-Brasil-blue.svg" alt="Feito no Brasil">
</p>

---

## 🚀 O que é a DevLoad?

A **DevLoad** é uma rede social de desktop desenvolvida em **Python**, criada para que desenvolvedores compartilhem ideias, projetos e trechos de código. Com interface gráfica baseada em **Tkinter** e banco de dados **MySQL** (compatível com MariaDB), o projeto possui arquitetura limpa e modular, separada em camadas de serviço, repositório e UI, tornando-se excelente para estudo e expansão.

---

## 🎬 Demonstração da Aplicação

Veja abaixo uma demonstração visual do funcionamento da DevLoad:

![Funcionamento da DevLoad](https://raw.githubusercontent.com/henriquetourinho/devload/main/media/funcionamento.gif)

---

## 🛠️ Instalação e Uso

Siga os passos abaixo para configurar e executar o projeto DevLoad no seu ambiente.

### 1. Pré-requisitos

Garanta que as seguintes ferramentas estejam instaladas em seu sistema (Debian/Ubuntu):

```bash
sudo apt update && sudo apt install git python3 python3-pip python3-venv mariadb-server
```
*A aplicação usa o conector MySQL, compatível com MariaDB.*

---

### 2. Configuração do Banco de Dados

Crie o banco de dados e usuário para a aplicação:

```bash
# Acesse o console do MySQL/MariaDB como root
sudo mysql -u root

# No prompt do MySQL, execute:
CREATE DATABASE devload;
CREATE USER 'devloaduser'@'localhost' IDENTIFIED BY 'sua_senha_segura_aqui';
GRANT ALL PRIVILEGES ON devload.* TO 'devloaduser'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

Importe a estrutura e dados de exemplo (opcional):

```bash
# Estrutura + dados de exemplo:
mysql -u devloaduser -p devload < devload_data.sql

# Ou apenas a estrutura:
mysql -u devloaduser -p devload < schema.sql
```

---

### 3. Instalação da Aplicação

Clone o repositório, configure o ambiente virtual e instale as dependências:

```bash
# 1. Clone o projeto
git clone https://github.com/henriquetourinho/devload.git

# 2. Entre na pasta do projeto
cd devload

# 3. Crie e ative um ambiente virtual
python3 -m venv venv
source venv/bin/activate

# 4. Instale as dependências Python
pip install -r requirements.txt
```

---

### 4. Configuração da Conexão

Ajuste as credenciais de conexão com o banco de dados:

```bash
# Copie o arquivo de exemplo:
cp config.py.example config.py

# Edite config.py com seu editor favorito
nano config.py

# Altere DB_PASSWORD para a senha definida no passo 2.
```

---

### 5. Execução

Execute a aplicação:

```bash
# Certifique-se de que o ambiente virtual (venv) está ativo
python3 main.py
```

---

## 🧩 Recursos Implementados

- **Arquitetura Profissional:** Código modular com camadas (UI, Serviços, Repositórios)
- **Autenticação de Usuários:** Login/Registro com senhas criptografadas via `werkzeug`
- **Timeline de Posts:** Lista rolável dos posts mais recentes
- **Composer Inline:** Caixa de publicação expandível na timeline
- **Sistema de Comentários:** Expanda posts para ver e adicionar comentários
- **Perfis de Usuário:** Exibição de foto, bio, links e detalhes
- **Edição de Perfil:** Formulário para atualização das informações do usuário
- **Interações:** Curtidas em posts com atualização dinâmica
- **Interface Tkinter:** UI de desktop funcional e estilizada

---

## 🔐 Segurança e Boas Práticas

- **Senhas Criptografadas:** Armazenadas com hashes seguros (`werkzeug`)
- **Configuração Segura:** Senha do banco em `config.py` (inclua no `.gitignore`)
- **Ambiente Virtual:** Uso de `venv` para isolar dependências

---

## 🤝 Apoie o Projeto

Se a **DevLoad** ajudou seus estudos ou serviu de base para outros projetos, apoie para manter a iniciativa ativa:

**Chave Pix:**  
```
poupanca@henriquetourinho.com.br
```

---

## 📄 Licença

Distribuído sob a **licença GPL-3.0**. Veja o arquivo `LICENSE` para detalhes.

---

## 🙋‍♂️ Desenvolvido por

**Carlos Henrique Tourinho Santana**  
📍 Salvador - Bahia  

- 🔗 [Wiki Debian](https://wiki.debian.org/henriquetourinho)
- 🔗 [LinkedIn](https://br.linkedin.com/in/carloshenriquetourinhosantana)
- 🔗 [GitHub](https://github.com/henriquetourinho)
