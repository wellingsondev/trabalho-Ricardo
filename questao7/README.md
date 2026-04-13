Cenário
Carolina controla em Excel uma planilha com a sua lista de compras mensal. O sistema deve permitir o cadastro de produtos, unidades de compra e quantidades, diferenciando o que é previsto para o mês do que será efetivamente comprado. O preço estimado é atualizado mensalmente por Carolina para refletir a realidade do mercado.

Resposta da Questão
A solução proposta utiliza duas classes principais conforme o diagrama UML:

Classe Produto: Encapsula os dados individuais e possui os métodos atualizarPrecoEstimado() e calcularTotalItem().

Classe ListaCompra: Atua como o container mensal, associando-se a um ou mais produtos (1..*) e sendo responsável pelo método CalcularTotalCompra().

A modelagem garante que Carolina possa ter várias listas (uma para cada mês referenciado) e que cada lista gerencie dinamicamente seu conjunto de produtos.