# Emissão de Certificado CNPJ - Site Receita Federal Brasileira

Solução captcha da Receita Federal.

![Exemplo de Captcha](https://user-images.githubusercontent.com/71271207/171506159-c5c2e472-2161-4883-a653-c4a5aa17ca59.png)

<hr>
Após diversas analises gráficas, e estatisticas e testando diversas soluções consegui encontrar uma forma de solucionar o Captcha, hoje a imagem com diversas ruídos e o audio também com muitos rúidos.

Em minhas tentativas utilizando essa solução estou com **100% de precisão**. Melhorias no código são bem-vindas.

*Aqui somente contem o código com a solução pronta, todos os gráficos e outras funções que foram utilizadas para analise e montar as funções para solução não estarão neste repositório.*

O Código deste repositório será utilizado com Selenium, as informações sobre as letras foram todas salvas em um arquivo JSON, que é necessários para realizar o reconhecimento das letras.

> Neste código não há comentários nem instruções dizendo o que estou fazendo em cada etapa, para entender alguns pontos será necessários um pouco mais de conhecimento em Python.

#### Requirements 
* numpy
* selenium
* requests
* scipy

#### Instruções de uso

Procurei deixar tudo em único arquivo para facilitar a utilização de quem não está habituado a diversos arquivos.

1. Instale o repositório, e confirme o caminho do seu WebDriver do Selenium
2. A utilização de Cookies é de extrama importancia, para download do audio do Captcha


### Informações sobre analise

Primeiro descarte foi a analise de imagem, a mais de um ano já estava aprendendo sobre imagens e tratamento em python, até utilizei esse captcha e do Detran PR, como laboratório para aprendizagem, mas muito processamento para pouco resultado, apos todo tratamento vem toda a parte de aprendizado de máquina (Machine Learning), para você ainda não possuir precisão de 100%.

#### 1. Analise Gráfica

Verificando gráfico com fala das letras e ruidos

