# Emissão de Certificado CNPJ - Site Receita Federal Brasileira

Solução captcha da Receita Federal.

Após diversas analises gráficas, e estatisticas e testando diversas soluções consegui encontrar uma forma de solucionar o Captcha, hoje a imagem com diversas ruídos e o audio também com muitos rúidos.

Não encontrei falhas, das minhas tentativas está dando 100% de precisão.

*Aqui somente contem o código com a solução pronta, todos os gráficos e outras funções que foram utilizadas para analise e montar as funções para solução não estarão neste repositório.*

O Código deste repositório será utilizado com Selenium, as informações sobre as letras foram todas salvas em um arquivo JSON, que é necessários para realizar o reconhecimento das letras

#### Requirements 
* numpy
* selenium
* requests
* scipy

#### Instruções de uso

1. Instale o repositório, e confirme o caminho do seu WebDriver do Selenium
2. A utilização de Cookies é de extrama importancia, para download do audio do Captcha
3. 
