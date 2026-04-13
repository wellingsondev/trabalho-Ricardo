Questão – Sistema de Pessoas, Clientes e Funcionários
 Descrição

O sistema tem como objetivo gerenciar informações de pessoas, incluindo clientes e funcionários.

Cada pessoa possui dados básicos como nome e data de nascimento, além de estar associada a endereços e telefones.

Clientes possuem informações adicionais como código, limite e data de compra, além de estarem associados a uma profissão.

Funcionários possuem matrícula, salário e data de admissão, além de estarem associados a um cargo.
Solução

Foram identificadas as seguintes classes:

- Pessoa
- Cliente
- Funcionario
- Endereco
- Telefone
- Profissao
- Cargo

A classe Pessoa é a base do sistema, sendo especializada pelas classes Cliente e Funcionario.

A classe Endereco e Telefone estão associadas à Pessoa.

A classe Cliente está associada à Profissao.

A classe Funcionario está associada ao Cargo.

Funcionalidades

- Cadastro de pessoas
- Cadastro de clientes e funcionários
- Associação de endereços e telefones
- Associação de profissão ao cliente
- Associação de cargo ao funcionário
- Consulta de dados cadastrados
- Atualização e exclusão de registros

O sistema organiza de forma estruturada os dados de pessoas, clientes e funcionários,
permitindo gerenciamento eficiente e reutilização de informações por meio de herança
e relacionamentos entre classes.