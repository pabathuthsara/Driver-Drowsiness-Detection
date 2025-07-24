## Real-time Multi-Sensor Safety System for Vehicle Integration
[Link to Architecture Diagram](https://lucid.app/lucidchart/32cc0406-70f7-41dc-9af4-844296879085/edit?viewport_loc=-1240%2C-1101%2C2475%2C2083%2C0_0&invitationId=inv_8b8f6e9e-bf17-4b59-8de6-2f59f5599511)


A comprehensive drowsiness detection system that monitors driver alertness through facial analysis, heart rate tracking, and driving behavior patterns. The system provides immediate alerts when drowsiness is detected, helping prevent accidents caused by driver fatigue.

---

## System Architecture Flow Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                                Input sensors                                │
│                                                                             │
│  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────────────┐  │
│  │ Night Vison     │    │ BLE HR Wristband│    │    Accelerometer        │  │
│  │    Camera       │    │                 │    │                         │  │
│  └─────────────────┘    └─────────────────┘    └─────────────────────────┘  │
│           │                       │                         │               │
└───────────┼───────────────────────┼─────────────────────────┼───────────────┘
            │                       │                         │
            │                       │                         │
            ▼                       ▼                         ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                              Raspberrypi 5                                 │
│                                                                             │
│                           SOFTWARE MODULES                                 │
│                                                                             │
│  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────────────┐  │
│  │  Face detection │    │ HR Processing   │    │ Motion Processing       │  │
│  │     module      │    │    Module       │    │      Module             │  │
│  │                 │    │                 │    │                         │  │
│  │ -Eye aspect ratio│   │ -BLE data       │    │ -Driving pattern        │  │
│  │ -Blink frequency │   │  collection     │    │  analysis               │  │
│  │ -Yawn detection  │   │ -HR pattern     │    │ -Sudden movement        │  │
│  │ -Head tilt analysis│ │  analysis       │    │  detection              │  │
│  │                 │    │ -Anomaly        │    │ -Baseline comparison    │  │
│  │                 │    │  detection      │    │                         │  │
│  └─────────────────┘    └─────────────────┘    └─────────────────────────┘  │
│           │                       │                         │               │
│           └───────────────────────┼─────────────────────────┘               │
│                                   ▼                                         │
│                    ┌─────────────────────────────────┐                      │
│                    │      Sensor Fusion              │                      │
│                    │        Engine                   │◄─────────────────────┤
│                    │                                 │                      │
│                    │ -MultiModal analysis            │                      │
│                    │ -Threshold management           │                      │
│                    └─────────────────────────────────┘                      │
│                                   │                                         │
│                                   ▼                                         │
│                    ┌─────────────────────────────────┐                      │
│                    │   Alert Decision Engine         │                      │
│                    │                                 │                      │
│                    │ -Drowsiness score               │                      │
│                    │  calculation                    │                      │
│                    │ -Alert level calculation        │                      │
│                    │ -False positive filtering       │                      │
│                    └─────────────────────────────────┘                      │
│                                   │                                         │
└───────────────────────────────────┼─────────────────────────────────────────┘
                                    │
                                    │
                                    │          ┌─────────────────────────────┐
                                    │          │       Power Management      │
                                    │          │                             │
                                    │          │     12v Vehicle Power       │
                                    │          │                             │
                                    │          │ -Voltage regulation         │
                                    │          │ -Power distribution         │
                                    │          │ -Lower power mode           │
                                    │          └─────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                               Alert System                                 │
│                                                                             │
│                     │                     │                                │
│  ┌─────────────────┐│  ┌─────────────────┐│  ┌─────────────────────────────┐ │
│  │   Buzzer Alert  ││  │   Haptic Alert  ││  │      Visual Alert           │ │
│  │                 ││  │                 ││  │                             │ │
│  │                 ││  │                 ││  │                             │ │
│  └─────────────────┘│  └─────────────────┘│  └─────────────────────────────┘ │
└─────────────────────┴─────────────────────┴─────────────────────────────────┘
```

## How It Works

**1. Multi-Sensor Input Collection**
- **Night Vision Camera**: Captures facial features, eye movements, and head positioning even in low-light conditions
- **BLE Heart Rate Wristband**: Wirelessly monitors physiological indicators like heart rate variability
- **Accelerometer (MPU6050)**: Tracks vehicle movement patterns and detects erratic driving behavior

**2. Intelligent Processing on Raspberry Pi 5**
The system runs three specialized processing modules simultaneously:
- **Face Detection Module**: Analyzes eye aspect ratios, blink frequency, yawn detection, and head tilt
- **HR Processing Module**: Collects BLE data, analyzes heart rate patterns, and detects anomalies
- **Motion Processing Module**: Evaluates driving patterns, detects sudden movements, and compares against baseline behavior

**3. Advanced Sensor Fusion**
All sensor data streams are intelligently combined using multimodal analysis and dynamic threshold management to create a comprehensive drowsiness assessment.

**4. Smart Alert Decision Engine**
- Calculates real-time drowsiness scores
- Determines appropriate alert levels based on severity
- Filters false positives to prevent unnecessary alarms

**5. Multi-Modal Alert System**
When drowsiness is detected, the system activates:
- **Buzzer Alert**: Immediate audio warning
- **Haptic Alert**: Vibration through the wristband
- **Visual Alert**: LED indicators for additional awareness

## Key Benefits

- **Plug-and-Play Design**: Easy installation in any vehicle
- **Affordable Solution**: Cost-effective compared to factory systems
- **Real-Time Processing**: Immediate response to drowsiness indicators
- **Multi-Layer Detection**: Combines visual, physiological, and behavioral monitoring
- **Low Power Consumption**: Efficient 12V vehicle integration with power management

