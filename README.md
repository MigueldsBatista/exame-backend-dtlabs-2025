CRITÉRIOS DE AVALIAÇÃO 
- Velocidade de entrega do teste resolvido. 
- Qualidade dos testes. 
- Estrutura da aplicação. 
- Coerência com o que foi solicitado. 
- Tratamento de erros. 
- Status Code coerentes com a aplicação. 
- Documentação da API. 
- Uso de Design Patterns. 
- Uso correto dos verbos HTTP e Headers. 
- Design do Banco de Dados. 
- Documentação do repositório.

CASE 
Você irá desenvolver o backend de uma aplicação de IoT. Seu produto consiste em um servidor que está localizado on-premise no seu cliente. Este servidor coleta dados de diversos sensores. Os servidores enviam para um único banco de dados. Cada servidor comporta até 4 (quatro) sensores diferentes: 

- Sensor de Temperatura.
- Valores são medidos em graus celsius.

- Sensor de Umidade.
- Valores são medidos em %, de 0 a 100.

- Sensor de Tensão Elétrica.
- Valores são medidos em Volts.

- Sensor de Corrente Elétrica.
- Valores são medidos em Ampère.

É possível que um servidor tenha um sensor de temperatura e um sensor de umidade. Portanto, 
eles enviam os dois valores na mesma requisição. Cada servidor vai possuir apenas 1 (um) sensor de cada. 
Logo, não existem servidores que possuem 3 (três) sensores de temperatura e 1 (um) sensor de corrente elétrica. 
Os servidores podem enviar dados com uma frequência de, no mínimo, 1 Hz, e, no máximo, 10 Hz. 
A seguir, serão descritos os endpoints necessários para serem implementados e descritivo do que eles devem fazer.


#to run server use command: uvicorn main:app --reload

1. Autenticação (JWT)
O sistema deve ter um mecanismo de autenticação baseado em JWT para proteger endpoints privados. Os servidores e usuários autenticados devem utilizar um token para acessar as funcionalidades restritas.
Endpoints esperados:
● POST /auth/register → Criar um novo usuário.
● POST /auth/login → Autenticar usuário e retornar um token JWT.


- OQ falta

padronizar as respostas do servidor

verificar o status do servidor / ver se ele teve alguma atv nos ultimos 10 s

fazer as queries e agregacoes da funcao get data

implementar middlewares de autenticação

implementar o servidor que envia as requisicoes como um servico separado que pode ser iniciado e "Simula"
os iot's

implementar os testes
- testar mappers
- testar os servicos talvez

implementar sistema de check health
