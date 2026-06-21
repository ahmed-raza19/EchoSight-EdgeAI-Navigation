<div align="center">
  <h1>🚗 EchoSight</h1>
  <p><i>Autonomous Navigation & Real-Time Spatial AI System</i></p>

  ![ROS 2](https://img.shields.io/badge/ROS_2-Jazzy-blue?style=for-the-badge&logo=ros)
  ![Python](https://img.shields.io/badge/Python-3.12-yellow?style=for-the-badge&logo=python)
  ![YOLOv8](https://img.shields.io/badge/YOLOv8-Vision-orange?style=for-the-badge)
  ![Hardware](https://img.shields.io/badge/Hardware-Raspberry_Pi_4-C51A4A?style=for-the-badge&logo=raspberry-pi)

</div>

---

## 📖 Overview

**EchoSight** is a machine learning and robotics integration project designed to act as a highly responsive safety layer for visually impaired individuals. By fusing computer vision (YOLOv8) with spatial mapping (RPLiDAR), this system detects environmental hazards and executes split-second, autonomous hardware interventions to prevent collisions.

## ✨ Core AI & Software Features

* **Live Object Detection:** Utilizes the YOLOv8 model combined with OpenCV to process live camera feeds, identifying semantic context (e.g., people, vehicles, barriers) with near-zero latency.
* **Point-Cloud Data Filtering:** Custom spatial algorithms extract and clean raw LiDAR arrays. The system actively isolates the vehicle's forward vector, discarding infinite/`nan` values to construct an accurate map of solid obstacles.
* **Autonomous Decision Matrix:** A central ROS 2 control node fuses vision classifications and distance metrics. Breaching the dynamic 0.35-meter safety perimeter triggers an immediate, asynchronous hardware interrupt to halt the motor controllers.

## 🗂️ Project Structure

```text
EchoSight-AI-Navigation/
├── src/
│   ├── echosight_control.py   # Main decision logic & safety envelope
│   ├── lidar_node.py          # Spatial data filter and normalizer 
│   └── motor_drive.py         # GPIO hardware interfacing
├── models/
│   └── yolov8n.pt             # Pre-trained YOLOv8 weights (Add locally)
├── media/                   
│   └── demo.gif               # System demonstration (Add locally)
├── requirements.txt           # Python dependencies
└── README.md
```

## ⚙️ Tech Stack & Middleware

* **Languages:** Python 3, C++ (Underlying ROS dependencies)
* **AI/ML:** PyTorch, Ultralytics (YOLO), OpenCV
* **Middleware Framework:** ROS 2 (Jazzy Jalisco)
* **Hardware Interfacing:** `RPi.GPIO`, `rclpy`

## 🚀 Quick Start

**1. Clone the repository:**

```bash
git clone https://github.com/yourusername/EchoSight-AI-Navigation.git
cd EchoSight-AI-Navigation
```

**2. Install ML Dependencies:**

```bash
pip install -r requirements.txt
```

**3. Build the ROS 2 Workspace:**
*Assuming this repository is placed inside your `~/ros2_ws/src` folder.*

```bash
cd ~/ros2_ws
colcon build --packages-select echosight_pkg
source install/setup.bash
```

**4. Execute the Control Node:**

```bash
ros2 run echosight_pkg echosight_control
```

---

<div align="center">
  <i>Engineered for robust spatial awareness and low-latency robotics.</i>
</div>
