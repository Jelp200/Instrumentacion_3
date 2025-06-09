# System Architecture

## Arduino Side

- Generates pseudo-random sequence
- Multiplies it with the input signal
- Samples the result and sends it via Modbus

## LabVIEW Side

- Reads Modbus data
- Sends measurements to a Python node
- IRLS reconstructs the original sparse signal
- Results displayed on UI

```
[Signal] --x--> [Pseudo-Random] --> [ADC] --> [Modbus] --> [LabVIEW + IRLS] --> [UI]
```
