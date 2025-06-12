#  Aplicacao Distribuída com Sockets TCP na AWS

## 📌 Visão Geral

Este projeto implementa uma aplicação distribuída simples composta por:

- Um **servidor TCP** em uma instância EC2 que escuta dados de sensores;
- Dois **clientes TCP** (instâncias EC2) que simulam sensores de temperatura e umidade, enviando dados continuamente para o servidor.

A infraestrutura é provisionada via **AWS CloudFormation** utilizando um arquivo YAML.

---

## 🚀 Pré-requisitos

- Conta AWS ativa
- AWS CLI configurado com credenciais válidas
- Par de chaves EC2 (para acesso SSH se necessário)
- Permissões para criar VPCs, sub-redes, instâncias EC2, e Security Groups

---

## 💠 Como Inicializar a Infraestrutura

### 1. Clone o repositório (caso aplicável)

```bash
git clone https://github.com/JuIioSilva/ProjetoNuvem.git
cd ProjetoNuvem
```

### 2. Faça upload do template CloudFormation

Certifique-se de ter o arquivo `infraestrutura.yaml` salvo localmente. Em seguida, execute:

```bash
aws cloudformation create-stack \
  --stack-name AplicacaoTCPDistribuida \
  --template-body file://infraestrutura.yaml \
  --capabilities CAPABILITY_NAMED_IAM \
  --parameters ParameterKey=KeyName,ParameterValue=NomeDoSeuKeyPair
```

> Substitua `NomeDoSeuKeyPair` pelo nome do seu par de chaves EC2 existente.

---

## ⚙️ O que o CloudFormation irá criar

- Uma VPC com duas sub-redes públicas
- Um Internet Gateway e tabela de rotas
- Um Security Group permitindo acesso TCP na porta 5000
- Três instâncias EC2:
  - 1 servidor (porta 5000)
  - 2 clientes com scripts que conectam ao servidor
- Scripts Python executados automaticamente via `UserData`

---

## 🥺 Como Testar a Aplicação

### 1. Acompanhar os logs

Use o AWS Systems Manager (caso ativado) ou acesse via SSH:

```bash
ssh -i "sua-chave.pem" ec2-user@<IP-do-Servidor>
cat log.txt
```

Você verá mensagens como:

```
[2025-06-11 10:15:42] Nova conexão de ('10.0.2.135', 54812)
[2025-06-11 10:15:42] Recebido de ('10.0.2.135', 54812): Sensor1 - Temperatura: 25.34°C
```

### 2. Verificar processos dos clientes

Você pode também acessar os clientes via SSH para verificar se o script está rodando:

```bash
ps aux | grep client.py
```

### 3. Testes de carga (opcional)

Você pode duplicar a instância `EC2Client1` com o mesmo `UserData` para simular múltiplos sensores conectados ao mesmo servidor.

---

## 🚩 Como Destruir a Infraestrutura

```bash
aws cloudformation delete-stack --stack-name AplicacaoTCPDistribuida
```

---

## 💡 Dicas

- Verifique o status das instâncias via AWS Console ou com:

```bash
aws ec2 describe-instances --query "Reservations[*].Instances[*].[InstanceId,State.Name,PublicIpAddress]" --output table
```

- Certifique-se de que a porta 5000 esteja aberta no seu Security Group.

---

## 📌 Extras

- Você pode adaptar o projeto para usar protocolos como HTTP/gRPC.
- É possível integrar com banco de dados (RDS, DynamoDB).
- Adicionar Auto Scaling e Load Balancer para produção.

