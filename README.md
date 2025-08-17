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
| Raspberry Pi 5                 | Main processing + ML                 |
| Night-vision camera module  | For face and eye tracking            |
| BLE heart rate wristband    | Wireless HR monitoring               |
| MPU6050                     | 3-axis accelerometer + gyroscope     |
| Buzzer                      | Alerts on drowsy detection           |

---

## 12-Week Development Timeline

| **Week** | **Milestone / Task**                                                                 | **Status** |
|----------|----------------------------------------------------------------------------------------|------------|
| 1        | Set up GitHub repo, finalize parts list, confirm vendors, create system design draft | ✅ Complete |
| 2        | Place hardware orders, start architecture diagrams, plan BLE HR data format            | ✅ Complete |
| 3        | Hardware arrives → unbox + test: Pi/Jetson, sensors, wristband                         | ✅ Complete |
| 4        | Set up Pi and dependencies, run test camera                                            | ✅ Complete |
| **5**    | **Deploy facial landmark detection code to Raspberry Pi, begin heart rate integration** | 🔄 **Current Week** |
| 6        | Complete heart rate data collection and BLE communication setup                        |            |
| 7        | Develop basic accelerometer data reading logic                                         |            |
| 8        | Integrate sensor streams: face data + HR + acceleration                                |            |
| 9        | Develop alerting system (buzzer on drowsiness detection)                               |            |
| 10       | Begin in-vehicle testing: gather sample data during day + night                        |            |
| 11       | Optimize ML model thresholds (+ fallback rules), fix false alerts                      |            |
| 12       | Final testing, wrap-up documentation, create demo video, project report                |            |

---

## Current Progress Summary

### ✅ **Completed (Weeks 1-4)**
- Hardware procurement and setup
- Raspberry Pi 5 configuration with required dependencies
- Camera module testing and verification
- Facial landmark detection code development (OpenCV/Dlib)
- Eye aspect ratio and blink detection algorithms implemented
- Heart rate integration research completed

### 🔄 **Week 5 - Current Focus**
- **Primary Goal**: Deploy facial landmark detection system to Raspberry Pi
- **Secondary Goal**: Begin heart rate wristband integration
- **Key Tasks**:
  - Optimize facial detection performance on Pi hardware
  - Test real-time processing capabilities
  - Initialize BLE communication with heart rate wristband
  - Validate heart rate data collection protocols

### 📋 **Upcoming Priorities (Weeks 6-7)**
- Complete heart rate sensor integration and data streaming
- Implement accelerometer data collection from MPU6050
- Begin multi-sensor data fusion architecture








