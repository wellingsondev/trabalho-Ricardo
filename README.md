# trabalho-Ricardo

questão numero 1:

Foi desenvolvido um sistema para controle de gastos mensais de energia elétrica,
permitindo o cadastro das contas de luz e a realização de consultas como:

- Identificação do mês de menor consumo
- Identificação do mês de maior consumo

O sistema também calcula automaticamente a média de consumo mensal,
facilitando o acompanhamento dos gastos.

questao número 2:
O exercício tem como objetivo a criação de uma classe chamada "TextoSaida",
que permite configurar a exibição de um texto com diferentes propriedades,
sem depender de uma linguagem específica ou de componentes visuais reais.

O usuário pode definir características como tamanho da letra, cor da fonte,
cor de fundo e o tipo de componente onde o texto será exibido.

solução

Foi modelada a classe "TextoSaida", contendo atributos e métodos responsáveis
pela configuração e exibição do texto.

A classe permite:

- Definir o texto a ser exibido
- Configurar o tamanho da letra
- Escolher a cor da fonte e do fundo
- Selecionar o tipo de componente (label, edit ou memo)

Também foram implementadas validações para garantir que:

- As cores estejam entre as opções permitidas (preto, branco, azul, amarelo e cinza)
- O tipo de componente seja válido

questão número 3:
 Cenário
Este projeto faz parte de um exercício acadêmico proposto pelo Professor Ricardo Roberto. O objetivo é criar uma classe que represente um boneco capaz de se movimentar em uma tela, gerenciando suas coordenadas espaciais e sua orientação.
Atributos do Boneco:
- **Nome:** Identificação do personagem.
- **Coordenada X:** Posição horizontal na tela.
- **Coordenada Y:** Posição vertical na tela.
- **Direção Atual:** Pode assumir os valores: `Cima`, `Baixo`, `Direita` ou `Esquerda`.

Resposta da Questão
A solução consiste na criação da classe `Boneco`, contendo métodos para mover o objeto e alterar sua direção, garantindo o encapsulamento dos dados de posição.

questão número 4 :

Cenário 
Este projeto consiste em uma aplicação de controle pessoal para smartphones, projetada para auxiliar o usuário (neste caso, Maurício) a gerenciar o uso de medicamentos prescritos, evitando esquecimentos e organizando a rotina de saúde.

Resolução
A lógica da aplicação foca no gerenciamento de datas e horas. A entidade principal armazena o estado do tratamento, enquanto uma função de "reorganização" é disparada sempre que o horário real de consumo difere do horário planejado, garantindo que o intervalo entre as doses seja respeitado.

