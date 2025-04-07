# Sistema de Medição Ultrassônica – Rio Pomba

Projeto desenvolvido com ESP32 e Sensor Ultrassônico A01 (Switch Output) para monitoramento do nível do Rio Pomba. Atualmente, os dados são disponibilizados por meio de um servidor web local, e futuramente estarão acessíveis em um site público com atualização em tempo real via MQTT.

O objetivo é oferecer à população uma plataforma acessível para acompanhar o nível do Rio Pomba — o principal rio da cidade — que, especialmente no período de chuvas, frequentemente transborda e causa prejuízos significativos. A solução busca fornecer uma alternativa moderna à consulta presencial da régua localizada na Avenida Élcio Silveira Siqueira, permitindo que moradores se preparem com antecedência para possíveis enchentes.


## Como usar

1. Faça upload dos arquivos para o ESP32 com MicroPython (testado em Micropython v1.24.1).
2. Reinicie o dispositivo.
3. Conecte-se à rede Wi-Fi **PombaRiver** (sem senha).
4. Acesse `http://192.168.4.1` para visualizar o nível atual em centímetros.

## Sensor Utilizado

- **Modelo**: A01NYUB (DFRobot) – saída digital tipo *switch output* (nível lógico muda conforme distância).
- **Faixa de medição**: 300 mm a 7500 mm.
- **Alimentação**: 5VDC.
- **Precisão**: Ajustável em etapas (500mm, 100mm, 10mm).

## Atualização

- Medições realizadas continuamente e atualizadas a cada 5 segundos na interface web.

## Autor

Matheus V. Holender, em parceria com Eneltec Ltda.
