# Driver Drowsiness Detection System

An affordable, plug-and-play driver drowsiness detection system that monitors real-time facial features, heart rate (via wireless wristband), and driving patterns using accelerometer data to alert drivers and potentially prevent road accidents.

---

## Features

- Real-time **video-based drowsiness detection** (blinks, yawns, head tilt)
- **Wireless heart rate monitoring** via BLE wristband
- **Driving behavior tracking** via accelerometer (erratic movements)
- **Alert system** (buzzer/vibration) when drowsiness is detected
- Designed to be **affordable and compatible with any vehicle**

---

## Hardware Components

| Component                    | Specification                        |
|-----------------------------|--------------------------------------|
| Jetson Nano                 | Main processing + ML                 |
| Night-vision camera module  | For face and eye tracking            |
| BLE heart rate wristband    | Wireless HR monitoring               |
| MPU6050                     | 3-axis accelerometer + gyroscope     |
| Buzzer                      | Alerts on drowsy detection           |

---

## 12-Week Development Timeline

| **Week** | **Milestone / Task**                                                                 |
|----------|----------------------------------------------------------------------------------------|
| 1        | Set up GitHub repo, finalize parts list, confirm vendors, create system design draft |
| 2        | Place hardware orders, start architecture diagrams, plan BLE HR data format            |
| 3        | Hardware arrives → unbox + test: Pi/Jetson, sensors, wristband                         |
| 4        | Set up Pi/Jetson OS and dependencies, run test camera + sensors individually           |
| 5        | BLE heart rate monitoring integration (test data acquisition from wristband)           |
| 6        | Develop basic accelerometer data reading logic                                         |
| 7        | Facial landmark detection (OpenCV/Dlib): eye aspect ratio, blinking test code          |
| 8        | Integrate sensor streams: face data + HR + acceleration                                |
| 9        | Develop alerting system (buzzer on drowsiness detection)                               |
| 10       | Begin in-vehicle testing: gather sample data during day + night                        |
| 11       | Optimize ML model thresholds (+ fallback rules), fix false alerts                      |
| 12       | Final testing, wrap-up documentation, create demo video, project report                |

---

## Week 1 Task Plan (Next Week)

### Focus: Foundation & Planning

- [x] Initialize GitHub repository structure:
  - `/hardware` — Schematics, wiring diagrams
  - `/software` — Sensor code, model code
  - `/docs` — Architecture, references, testing notes
- [x] Add this README
- [x] Create basic wireframe or flowchart for system architecture
- [x] Finalize and confirm each component (with SL purchase links)
- [ ] Research BLE wristband data protocol (HR profile, UUIDs)
- [ ] Connect the rasberry pi 5 to the NoIR camera and test Face Landmark Detection & Pose Estimation by OpenCV




