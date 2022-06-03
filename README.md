# Emissão de Certificado CNPJ - Site Receita Federal Brasileira

Solução captcha da Receita Federal.

![Exemplo de Captcha](https://user-images.githubusercontent.com/71271207/171506159-c5c2e472-2161-4883-a653-c4a5aa17ca59.png)

Após diversas analises gráficas, e estatisticas e testando diversas soluções consegui encontrar uma forma de solucionar o Captcha, hoje a imagem com diversas ruídos e o audio também com muitos rúidos.

Em minhas tentativas utilizando essa solução estou com **100% de precisão**. Melhorias no código são bem-vindas.

*Aqui somente contem o código com a solução pronta, todos os gráficos e outras funções que foram utilizadas para analise e montar as funções para solução não estarão neste repositório.*

O Código deste repositório será utilizado com Selenium, as informações sobre as letras foram todas salvas em um arquivo JSON, que é necessários para realizar o reconhecimento das letras.

##### Potenciais de Melhorias
* Separação das letras no audio;
* Exportação do comprovante para PDF.

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

#### Exemplo
Utilizar o arquivo, cnpj.py

```
# Iniciar o objeto
cnpj = RFB_CNPJ() 

# Função para alterar caminho do ChromeDriver
# Padrão chomedriver/chromedriver.exe
# cnpj.config('chromedriver.exe') 

# Buscando CNPJ que almeja o certificado
cnpj.get('00000000000191', show = True) 

```
Neste exemplo deixei o computador mostrar o chrome trabalhando, mas por padrão o argumento show é Falso, ou seja, não irá mostrar, só irá aparecer o html em sua pasta.



## Informações sobre analise

Abaixo informações espero que contribuam com novos pensamento ou contribuições desta solução.

Primeiro descarte foi a analise de imagem, a mais de um ano já estava aprendendo sobre imagens e tratamento em python, até utilizei esse captcha e do Detran PR, como laboratório para aprendizagem, mas muito processamento para pouco resultado, apos todo tratamento vem toda a parte de aprendizado de máquina (Machine Learning), para você ainda não possuir precisão de 100%.

### 1. Analise Gráfica

Verificando gráfico com fala das letras e ruidos

##### Captcha: AAYHFF
![image](https://user-images.githubusercontent.com/71271207/171776952-56d05746-574c-46a4-974e-652a6266760f.png)
*De alguns captchas que baixei, utilizei esse como referencia, pois ter letras iguais no mesmo audio*

> Porem como podemos observar mesmo sendo a mesma letra, elas estão deslocadas em altura, ou seja, não são exatamente os mesmos números.**

Após isso, utilizei um gráfico que montei para realizar analises numéricas, para entender alguns números.

![image](https://user-images.githubusercontent.com/71271207/171777075-5a849526-b4de-417c-bc32-e95d1970cc0b.png)

Acabei verificando vários captchas, e observei que geralmente a distribuição de números negativos e positivos ficam em 50%, como podem observar na imagem, e variação dos intervalos de ruidos é de -3000 até 5000, mas geralmente a variação dela é de 5000, ou seja, em alguns casos ele gera um ruido de -1000 até 4000, em outros pode gerar de -3000 até 2000, que serão onde estarão lotados 50% dos nossos valores, ou seja, ruidos.

Outros indicadores também chamaram a atenção como o Coeficiente de Variação, estar baixo, mas não consegui chegar a grandes conclusões.

#### Separação das Letras:
Como observado, pelo mais lógico utilizei como referencia a dimensão do ruido para realizar a separação das letras, apos alguns ajustes, consegui chegar ao seguinte gráfico, utilizando pontos de referencia -4000 e 5000 como intervalo de ruidos.


**Em vermelho o Inicio de cada letra e em Roxo o final:**
![image](https://user-images.githubusercontent.com/71271207/171778085-5946cc5a-dcd4-43f4-8ad4-6424befd5115.png)

Observamos que possuimos um corte alem do imaginado, acaba acusando 7 letras, mas na verdade é a nossa letra Y

