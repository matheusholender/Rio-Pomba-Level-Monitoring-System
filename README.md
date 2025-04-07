# Sistema de Medição Ultrassônica – Rio Pomba

Projeto com ESP32 e Sensor Ultrassônico A01 (Switch Output) para monitoramento do nível do Rio Pomba. Atualmente, os dados são disponibilizados via webserver local. Futuramente, estarão acessíveis em um site público com atualização em tempo real via MQTT.
O projeto visa disponibilizar à população da cidade uma plataforma para consultar o nível do Rio Pomba, o rio mais importante da cidade mas que em várias ocasiões, principalmente na época das chuvas, transborda e causa danos muitas vezes irreparáveis à população.

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
