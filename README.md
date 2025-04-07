# Sistema de Medição Ultrassônica – Rio Pomba

Sistema embarcado para medição do nível do Rio Pomba com ESP32 e Sensor Ultrassônico A01 Switch Output, com transmissão de dados via MQTT (em construção, utilizando no momento apenas webserver local).

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
