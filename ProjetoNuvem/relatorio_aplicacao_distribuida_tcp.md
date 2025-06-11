# Relatório Técnico: Aplicação Distribuída com Sockets TCP na AWS

## 1. Introdução e Motivação

O presente projeto visa demonstrar a implementação de uma aplicação distribuída simples utilizando comunicação via sockets TCP entre um servidor e dois clientes. O cenário simula sensores que enviam dados a um servidor central para processamento, uma abordagem comum em IoT, monitoramento e sistemas distribuídos de coleta de dados.

A motivação é proporcionar uma base de aprendizado para comunicação em rede, implantação de infraestrutura automatizada na nuvem (AWS) e boas práticas de paralelismo e escalabilidade.

---

## 2. Arquitetura Proposta

A arquitetura é composta por:

- **VPC personalizada** com duas sub-redes (clientes e servidor);
- **Instância EC2 (servidor)** escutando conexões TCP na porta 5000;
- **Duas instâncias EC2 (clientes)** que simulam sensores de temperatura e umidade;
- **Security Group** permitindo tráfego TCP na porta 5000;
- **Internet Gateway** para acesso à Internet.

### Diagrama de Arquitetura

```plaintext
         Internet
             |
      +------+------+
      |  InternetGW  |
      +------+------+
             |
           VPC
             |
   +---------+----------+
   |                    |
 SubnetServidor     SubnetCliente
   |                    |
[EC2 - Server]   [EC2 - Client1, Client2]
```

---

## 3. Justificativa das Escolhas Tecnológicas

- **AWS CloudFormation**: facilita a gestão de infraestrutura como código.
- **EC2 Amazon Linux 2**: compatível com Python, estável e de baixo custo.
- **Sockets TCP**: comunicação direta e simples entre instâncias, sem necessidade de middleware.
- **Paralelismo com threads**: o servidor atende várias conexões simultaneamente.
- **UserData**: inicialização automatizada dos scripts.

Temas utilizados:

- Infraestrutura como código
- Redes virtuais (VPC, sub-redes, SG)
- Computação distribuída
- Paralelismo

---

## 4. Detalhamento da Infraestrutura como Código

Trecho de criação de instância EC2 para servidor:

```yaml
EC2Server:
  Type: AWS::EC2::Instance
  Properties:
    InstanceType: t2.micro
    KeyName: !Ref KeyName
    ImageId: ami-0c02fb55956c7d316
    SubnetId: !Ref SubnetServer
    SecurityGroupIds:
      - !Ref SecurityGroupTCP
    UserData:
      Fn::Base64: !Sub |
        #!/bin/bash
        yum install -y python3
        (salva e executa server.py com sockets)
```

Clientes usam o IP do servidor dinamicamente:

```python
HOST = '${ServerIP}'
```

---

## 5. Comunicação entre Componentes

A comunicação é feita via **sockets TCP**:

- O servidor escuta em `0.0.0.0:5000`.
- Clientes conectam ao IP público do servidor na porta 5000.
- A cada mensagem enviada, o servidor responde com "Dados recebidos com sucesso."

---

## 6. Estratégias de Paralelismo e Escalabilidade

- **Multithreading no servidor**: cada nova conexão é tratada por uma nova thread.
- **Clientes autônomos**: operam em ciclos com `sleep`, gerando tráfego continuamente.
- A arquitetura pode ser expandida para usar Auto Scaling ou ALB com instâncias adicionais, se adaptado para HTTP ou gRPC.

---

## 7. Testes Realizados

### Testes funcionais

- Verificação da comunicação cliente-servidor.
- Log de mensagens recebidas.

### Testes de concorrência

- Execução simultânea de vários clientes.
- O servidor atendeu várias conexões sem queda.

### Resultados

- Sistema funcionou estavelmente com duas instâncias clientes.
- Baixa latência de resposta.

---

## 8. Considerações Finais e Melhorias Futuras

O projeto demonstrou de forma clara como construir e operar uma aplicação distribuída básica com comunicação TCP, utilizando AWS e infraestrutura como código.

### Possíveis melhorias

- Substituir TCP bruto por gRPC ou HTTP para maior extensibilidade.
- Incluir balanceador de carga (ALB) e Auto Scaling.
- Persistir dados em banco (RDS, DynamoDB).
- Adicionar observabilidade com CloudWatch ou Prometheus.

