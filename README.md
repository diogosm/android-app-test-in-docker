# android-app-test-in-docker

A english version of this tutorial is available on the end of this README.

# PT-BR

Este tutorial contempla o uso do appium, pytest e aplicações Android evitando ao máximo a instalação de software e usando o máximo de recursos disponíveis no docker. 

Além disso, este tutorial contempla usuários windows que usam docker dentro do WSL. No entanto, tais procedimentos devem ser similares no linux normalmente.

Etapas:

## Requisitos

Os únicos requisitos deste tutorial são a instalação prévia do adb [https://developer.android.com/tools/adb?hl=pt-br](https://developer.android.com/tools/adb?hl=pt-br) e a instalação do docker. 

## Passo 1 - Instalação do ADB (no ubuntu WSL)

Instale o adb também no ubuntu WSL. Esta etapa é necessária caso você use o Docker **APENAS** dentro do WSL!

``` bash
sudo apt-get install adb && sudo apt-get install android-tools-adb
```

## Passo 2 - Intalação da imagens Docker do appium

Dado que é necessário o uso de um servidor Appium, seja para acessar via pytest ou via Appium Inspector (que substitui o Appium Desktop) [[https://github.com/appium/appium-inspector](https://github.com/appium/appium-inspector)].

Execute o container principal do appium server. Mantenha no mínimo a porta 4723 aberta pois será usada no Appium Inspector e no pytest.

``` bash
docker run --privileged -d -p 5901:5901 -p 2222:22 -p 4723:4723 -v $(pwd)/sdk:/root -v /dev/kvm:/dev/kvm -v /dev/bus/usb:/dev/bus/usb --name appium-container appium/appium
```

## Passo 3 - Conecta o adb ao device real

Aqui iremos conectar um celular real (conectado ao windows) ao adb do windows e ao adb do ubuntu WSL.

### ADB no windows

Considerando que você possui o adb instalado no windows, abra um PowerShell e inicie um server ADB e set o tcp ip mode para o device conectado.

``` shell
./adb.exe kill-server
./adb.exe start-server
```

Inicie o tcp ip mode.

``` shell
./adb.exe tcpip 5555
```

Se precisar validar, verifique os devices conectados com `./adb.exe devices`. Você visualizará algo como:
![image](https://github.com/diogosm/android-app-test-in-docker/assets/1641686/1de7cf7e-1cf8-43e9-b35f-0ce53e6a205f)

### ADB no ubuntu WSL (opcional para quem usa docker no WSL)

Para conectar seu linux WSL ao device conectado ao windows, basta reiniciar a sessão adb e conectar ao device via IP. Primeiro reinicie a sessão

``` bash
sudo adb kill-server
```

Verifique o IP do seu device (Configurações -> sobre o telefone -> role até o final da pagina e irá aparecer o IP do dispositivo). Conecte ao ip usando a porta definida no adb do windows. Exemplo:

``` bash
sudo adb connect 192.168.100.28:5555
```

### Disclaimer

Se você usa docker no windows, utilize a sessão adb normal sem o modo tcp ip.

## Passo 4 - Verifique se o container do appium server visualiza o device

Para verificar se o appium server criado no Passo 1 está funcionando, verifique pelo container se ele visualiza o device.

``` bash
docker exec -it appium-container adb devices
```

Em caso de erro, você pode forçar a conexão:

``` bash
docker exec -it appium-container adb connect 192.168.100.28:5555
```

## Passo 5 - Instale o app

Utilizando já nosso container appium server (appium-container), instale o app usando o apk. Neste exemplot estou instalando um app de nome budgetwatch.

``` bash
docker cp protect.budgetwatch_28.apk appium-container:/tmp && docker exec -it appium-container adb install -t /tmp/protect.budgetwatch_28.apk
```

## Passo 6 - Teste o appium server

Para testar, basta instalar e abrir o app Appium Inspector, antigo Appium Desktop. Basta acessar localhost ou o IP do container se estiver full no linux. Não se esqueça de adicionar os parâmetros do aapPackage, da activity e a ferramenta de automação. Veja no exemplo abaixo:

![image](https://github.com/diogosm/android-app-test-in-docker/assets/1641686/6771dfc5-92c6-459f-9b73-bf72411ac5e1)

Pós conectado:

![image](https://github.com/diogosm/android-app-test-in-docker/assets/1641686/359db070-7258-41ea-a58b-a2eb4ed60575)

## Passo 7 - Configure seu pytest com Docker

Para rodar seu programa pytest com python usando appium e docker, primeiro crie uma imagem para um container docker. no Dockerfile disponível nesse repositório há a construção da imagem bem como a instalação do pacote do Appium necessário para execução e do pacote do pytest. Fique a vontade para customizar.

Por mim, construa a imagem e execute seu código, que será explicado no Passo 8.

``` bash
docker build -t my-appium-app . && docker run my-appium-app
```

Repare que este código executa um `pytest` com as flags de stacktrace e verbose ativadas (--pdb e -v). Se precisar executar apenas um teste específico dentro do seu código, ao invés de todos (comportamento padrão), mude o CMD para:

``` bash
CMD ["pytest","-rA", "-k", "test_app_expense_add_noName_noValue", "budget_test.py"]
```

No qual `-k teste` executa a função para realizar um teste, cujo nome é `teste`. Fique atento aos possíveis parâmetros do pytest.

Exemplo pós execução:

![image](https://github.com/diogosm/android-app-test-in-docker/assets/1641686/8aabcc82-4236-4284-b78a-b2b9948b6cf5)

## Passo 8 - Executando os testes com pytest

Agora que todo o ambiente está construído e executando, os principais passos restante estão associados ao seu código de teste. O principal deles está relacionado a execução, mude as variáveis de configuração para:

``` python
desired_caps = {}
desired_caps['platformName'] = 'Android'
desired_caps['appium:automationName'] = 'uiautomator2'
desired_caps['deviceName'] = '192.168.100.28:5555'   ## device via tcp ip mode
desired_caps['appPackage'] = 'protect.budgetwatch'
desired_caps['appActivity'] = '.MainActivity'
desired_caps['autoGrantPermissions'] = 'true'

capabilities_options = UiAutomator2Options().load_capabilities(desired_caps)

self.driver = webdriver.Remote('http://172.17.0.2:4723', options=capabilities_options)
self.driver.implicitly_wait(10)
```

**Lembre-se** de que tal teste está executando dentro de um container, logo ele não tem acesso a sua rede (localhost por exemplo, pois o localhost dele é o próprio container), então utilize o ip do container que está rodando ao Appium server ou appium-container. Para isso, verifique o IP do **container** usando:

``` bash
docker inspect appium-container
```

Procure por `IPAddress`. Exemplo:

![image](https://github.com/diogosm/android-app-test-in-docker/assets/1641686/213f39b9-4d3e-455d-bc7c-b60a85cf7dea)


# EN

Este tutorial 
