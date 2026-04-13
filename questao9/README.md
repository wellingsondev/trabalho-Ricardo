 Descrição

O cenário descreve um sistema de gerenciamento de CDs, onde um CD pode ser
uma coletânea (contendo vários músicos) ou não. Além disso, cada CD possui
uma lista de músicas, com suas respectivas durações.

O sistema também deve permitir consultas específicas, como identificar
quais CDs pertencem a um determinado músico e em quais CDs uma música está presente.

Solução

Foram identificadas três classes principais:

- CD
- Musico
- Musica

A classe CD possui informações sobre coletânea e se é duplo, além de manter
listas de músicos e músicas associadas.

A classe Musica armazena o nome da música e sua duração.

A classe Musico representa os artistas associados aos CDs.

Os relacionamentos permitem:

- Um CD possuir vários músicos (especialmente em coletâneas)
- Um CD possuir várias músicas
- Uma música pode estar presente em vários CDs
- Um músico pode estar associado a vários CDs