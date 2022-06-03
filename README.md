# Emissão de Certificado CNPJ - Site Receita Federal Brasileira

Solução captcha da Receita Federal.

![Exemplo de Captcha](https://user-images.githubusercontent.com/71271207/171506159-c5c2e472-2161-4883-a653-c4a5aa17ca59.png)

Após diversas análises gráficas, e estatísticas e testando diversas soluções consegui encontrar uma forma de solucionar o Captcha, hoje a imagem com diversas ruídos e o áudio também com muitos ruídos.

Em minhas tentativas utilizando essa solução estou com **100% de precisão**. Melhorias no código são bem-vindas.

*Aqui somente contém o código com a solução pronta, todos os gráficos e outras funções que foram utilizadas para análise e montar as funções para solução não estarão neste repositório. 
* O Código deste repositório será utilizado com Selenium, as informações sobre as letras foram todas salvas em um arquivo JSON, que é necessário para realizar o reconhecimento das letras.

##### Potenciais de Melhorias
* Separação das letras no áudio;
* Exportação do comprovante para PDF.

> Neste código não há comentários nem instruções dizendo o que estou fazendo em cada etapa, para entender alguns pontos serão necessários um pouco mais de conhecimento em Python.

#### Requirements 
* numpy
* selenium
* requests
* scipy

#### Instruções de uso

Procurei deixar tudo em único arquivo para facilitar a utilização de quem não está habituado a diversos arquivos.

1. Instale o repositório, e confirme o caminho do seu WebDriver do Selenium
2. A utilização de Cookies é de extrema importância, para download do áudio do Captcha

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



## Informações sobre análise

Abaixo informações espero que contribuam com novos pensamento ou contribuições desta solução.

Primeiro descarte foi a analise de imagem, a mais de um ano já estava aprendendo sobre imagens e tratamento em python, até utilizei esse captcha e do Detran PR, como laboratório para aprendizagem, mas muito processamento para pouco resultado, apos todo tratamento vem toda a parte de aprendizado de máquina (Machine Learning), para você ainda não possuir precisão de 100%.

### 1. Analise Gráfica

Verificando gráfico com fala das letras e ruídos

##### Captcha: AAYHFF
![image](https://user-images.githubusercontent.com/71271207/171776952-56d05746-574c-46a4-974e-652a6266760f.png)
*De alguns captchas que baixei, utilizei esse como referencia, pois ter letras iguais no mesmo áudio*

> Porem como podemos observar mesmo sendo a mesma letra, elas estão deslocadas em altura, ou seja, não são exatamente os mesmos números.**

Após isso, utilizei um gráfico que montei para realizar análises numéricas, para entender alguns números.

![image](https://user-images.githubusercontent.com/71271207/171777075-5a849526-b4de-417c-bc32-e95d1970cc0b.png)

Acabei verificando vários captchas, e observei que geralmente a distribuição de números negativos e positivos ficam em 50%, como podem observar na imagem, e variação dos intervalos de ruídos é de -3000 até 5000, mas geralmente a variação dela é de 5000, ou seja, em alguns casos ele gera um ruido de -1000 até 4000, em outros pode gerar de -3000 até 2000, que serão onde estarão lotados 50% dos nossos valores, ou seja, ruídos.

Outros indicadores também chamaram a atenção como o Coeficiente de Variação, estar baixo, mas não consegui chegar a grandes conclusões.

#### Separação das Letras:
Como observado, pelo mais lógico utilizei como referência a dimensão do ruido para realizar a separação das letras, após alguns ajustes, consegui chegar ao seguinte gráfico, utilizando pontos de referência -4000 e 5000 como intervalo de ruídos.


**Em vermelho o Início de cada letra e em Roxo o final:**
![image](https://user-images.githubusercontent.com/71271207/171778085-5946cc5a-dcd4-43f4-8ad4-6424befd5115.png)

Observamos que possuímos um corte além do imaginado, acaba acusando 7 letras, mas na verdade é a nossa letra Y e mesmo utilizando algumas correções para este caso quando iniciamos os testes com mais captchas ele se perde fácil e acaba fazendo várias quebras, quebrando letras no meio.


Então após algumas tentativas, e diversas análises acabei ampliando o gráfico e verificando uma outra forma de separar ruídos de falas, abaixo as duas imagens que exemplificam isso.

##### Trecho somente com Ruídos
![image](https://user-images.githubusercontent.com/71271207/171868382-7ffe9b41-6dd7-4f64-9901-c779e66200cf.png)

Observe como os números estão bem parecidos, o intervalo de ruido os números são bem homogêneos.

##### Trecho de Fala
![image](https://user-images.githubusercontent.com/71271207/171869315-10af7d41-af33-4ce9-90f0-dddbde630662.png)

Aqui podemos observar a diferença, temos diversos números distintos.

Devido a isso, fiz a analise visando a verificação de números distintos e refiz a função para remover ruídos e separar letras, utilizando como parâmetro a busca de números homogenios, onde acabo encontrando muitas ocorrências parecidas sei que estamos tratando um intervalo de letra com ruídos.

##### Após a aplicar função de remover ruídos. * Essa função pode ser melhorada, pois para alguns captchas ainda pega muito ruido.
![image](https://user-images.githubusercontent.com/71271207/171873342-c7a54563-6a13-4d28-ba48-185441d67dac.png)

Eliminando o ruídos entre as letras, fica fácil separa-las para iniciar a fase de reconhecimento, pois além de identificar os ruídos também zerei os intervalos de ruídos.

Em seguida inicie o processo de comparação, e encontrei outro problema, devido aos ruídos as letras não possuem os mesmo números, a mesma letra A.

##### Mesma letra A
![image](https://user-images.githubusercontent.com/71271207/171936985-d85948d6-055b-4e67-9805-b47b2bcc997a.png)

### 2. Analise Numérica

Realizando a comparação de arrays, percentual de igualdade é mínimo, então começou a segunda parte do desafio encaixar os dois A, para consegui comparar, observando o gráfico, fica fácil a comparação entretanto quando observando os arrays não são muito parecidos.

Apos algumas pesquisas na internet, procurando alguns funções de redução de ruídos, não consegui nada muito preciso.

Depois de pensar um bom tanto, me toquei que poderia pegar os picos e também as baixas de cada letra, então fiz um teste com os 30 maiores valores e 30 menores, e comecei a comparar os arrays, realizando a subtração visando a diferença, devido ao nível de ruido de cada captcha, nunca teremos o zero como referencia de igualdade, em alguns casos a diferença da uns 2000 de cada letra, mas gerando números bem homogêneos, então independente do valor que seja 1 mil ou 2 mil ou 3 mil ou até mesmo 0, utilizei como referência o **Desvio Padrão**, quanto menor o desvio meais parecido os números são, então realizei analise manual com diversas letras.

Com tudo funcionando, devido aos benditos ruídos, nem todos os números batem, então estabeleci um desvio de padrão inferior a 10, por segurança mesmo que quando é uma letra diferente o desvio padrão é superior a 100 em alguns casos até 2000.

Agora ficou fácil, bastou coletar a informações de todos os dígitos e montar um banco de dados com essas informações para comparações, montei um JSON e inicie os testes e a precisão ficou muito boa.

<br>
@Ney Moresco
