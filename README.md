<div align="center">

# 🤖 EchoSight
### AI-Powered Autonomous Navigation Rover for the Visually Impaired

[![Python](https://img.shields.io/badge/Python-3.12-yellow?style=for-the-badge&logo=python)](https://python.org)
[![YOLOv8](https://img.shields.io/badge/YOLOv8n-Vision-orange?style=for-the-badge)](https://ultralytics.com)
[![DeepSORT](https://img.shields.io/badge/DeepSORT-Tracking-purple?style=for-the-badge)](https://github.com/nwojke/deep_sort)
[![Raspberry Pi](https://img.shields.io/badge/Raspberry_Pi_4-Hardware-C51A4A?style=for-the-badge&logo=raspberry-pi)](https://raspberrypi.com)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)

*A rover that sees, thinks, and guides — so the user doesn't have to.*

---

</div>

## 📸 The Build


| The Rover | The Goggles |
|:---------:|:-----------:|
| * <img width="767" height="705" alt="WhatsApp Image 2026-06-22 at 5 06 27 PM" src="https://github.com/user-attachments/assets/1d02a7fc-60b0-4522-92ae-0832a8c9f549" />
* | *<img width="1600" height="936" alt="WhatsApp Image 2026-07-22 at 4 35 05 PM - Edited" src="https://github.com/user-attachments/assets/ca66f6a1-5db9-45bb-b486-97f26be0f650" /> *
 |

---

## 🧭 What Is EchoSight?

Imagine walking through a crowded hallway completely blind. You don't know if there's a chair two feet ahead, a staircase around the corner, or someone crossing your path. You're dependent on a cane or another person just to get from one room to another.

EchoSight is our answer to that problem.

It's an autonomous rover that acts as an intelligent guide for visually impaired individuals. The rover leads the way — detecting obstacles in real time, tracking the user from behind, announcing what's around them through voice cues, and replanning its path if something blocks the way. The user just walks. The rover handles the rest.

This project was built as part of our AI and Robotics coursework at FAST NUCES Islamabad, but we wanted it to be more than just a course submission — we wanted it to actually work.

---

## 🎬 Demo

> *https://drive.google.com/file/d/1FF9CtHqbxq1pq8Tp9HdqUXWk8n4GvDZg/view?usp=drivesdk*

---

## ⚙️ How It Works — System Overview

EchoSight is built on three layers that work together:

**1. Sensing** — The RPLidar A2 scans the environment 360° at 10 times per second. DroidCam streams live video from the phone. A downward-tilted ultrasonic sensor watches for steps and drops.

**2. Thinking** — YOLOv8n identifies objects in the camera feed. DeepSORT assigns each detected person a persistent ID so the rover knows exactly which person to follow even in a crowd. A custom A\* planner builds a path to the destination and replans in real time if obstacles appear.

**3. Acting** — The rover drives using L298N-controlled DC motors. A speaker announces what's happening. The user-worn ESP32 goggles vibrate and beep independently as a close-range fallback alert system.

```
┌──────────────────────────────────────────────────────────────────┐
│                        EchoSight System                          │
│                                                                  │
│  ┌─────────┐   ┌──────────┐   ┌───────────┐   ┌─────────────┐  │
│  │ RPLidar │──▶│ Obstacle │   │  DroidCam │──▶│  YOLOv8n   │  │
│  │   A2    │   │ Mapping  │   │  (Phone)  │   │  DeepSORT  │  │
│  └─────────┘   └────┬─────┘   └───────────┘   └──────┬──────┘  │
│                     │                                  │         │
│                     ▼                                  ▼         │
│              ┌─────────────────────────────────────────────┐     │
│              │          Raspberry Pi 4 — Main Brain        │     │
│              │  A* Path Planner │ State Machine │ TTS      │     │
│              └──────────────────────┬──────────────────────┘     │
│                                     │                            │
│            ┌────────────────────────┼───────────────┐           │
│            ▼                        ▼               ▼           │
│       ┌─────────┐            ┌────────────┐   ┌──────────┐      │
│       │ L298N + │            │  Speaker / │   │  ESP32   │      │
│       │  Motors │            │  Earpiece  │   │  Goggles │      │
│       └─────────┘            └────────────┘   └──────────┘      │
└──────────────────────────────────────────────────────────────────┘
```

---

## 🤖 AI Models Used

### YOLOv8n — Object Detection
We used the pretrained YOLOv8 nano model for real-time object detection from the DroidCam video stream. It identifies people, chairs, doors, and other obstacles, and the rover announces them spatially — for example, *"chair on your right"* — so the user knows what's around them even without seeing it.

We chose YOLOv8n specifically because it's the lightest variant in the YOLO family, fast enough to run on a Raspberry Pi 4 without crippling the rest of the system.

### DeepSORT — Person Tracking & ID Assignment
YOLO detects, but DeepSORT *remembers*. When the rover locks onto the user at the start of a session, DeepSORT assigns them a persistent ID. Even if the user briefly steps out of frame or is partially occluded by another person, DeepSORT re-identifies them and keeps following the right person.

This is what makes the rover reliable in real environments rather than just empty hallways.

### Custom A\* Pathfinding — Real-Time Navigation
The A\* planner runs entirely on the Pi. It builds an occupancy grid from the LiDAR scan data and computes an optimal path to the destination. If an obstacle suddenly appears mid-path, the grid updates and the planner replans on the fly — no human input needed.

This is the core of the navigation logic and the part we're most proud of building from scratch.

---

## 🔧 Hardware

| Component | Role |
|-----------|------|
| **Raspberry Pi 4 Model B** | The brain — runs all Python code, AI models, and the state machine |
| **Slamtec RPLidar A2** | 360° laser scanner, 10 Hz, detects all obstacles around the rover |
| **L298N Motor Driver + DC Motors** | Drives the wheels with PWM speed control |
| **DroidCam (Phone as Webcam)** | Streams live video to the Pi; also used to lock in and store the user's person ID |
| **ESP32 + HC-SR04 Ultrasonic** | Worn by the user as goggles — independent buzzer and vibration alerts |
| **Tilted ToF / Ultrasonic Sensor** | Mounted pointing slightly downward — detects drops and downward stairs |
| **Speaker / Earpiece** | Delivers real-time voice guidance to the user |

> *(Add a wiring/component layout photo here)*

---

## 🧠 State Machine

The rover runs on a clean state machine — not just a script that drives forward. Every situation has a defined response:

```
  ┌────────┐
  │  IDLE  │ ──── User detected ────▶ ┌────────┐
  └────────┘                          │  PLAN  │ ──── Path found ────▶ ┌────────┐
                                      └────────┘                        │  LEAD  │
                                                                        └───┬────┘
                        ┌────────────────────────────────────────────────┐  │
                        │              During LEAD:                      │  │
                        │  User too close  ──▶ speed up                 │◀─┘
                        │  User falls behind ──▶ WAIT                  │
                        │  User lost (>3s)   ──▶ announce + WAIT       │
                        │  Obstacle < 40cm   ──▶ hard stop + WARN      │
                        │  Drop detected     ──▶ hard stop + WARN      │
                        │  Path blocked      ──▶ REPLAN                │
                        │  Goal reached      ──▶ ARRIVED               │
                        └────────────────────────────────────────────────┘

  WAIT ──── user resumes ────▶ LEAD
  WARN ──── path clears  ────▶ LEAD
  REPLAN ── new path found ──▶ LEAD
  ARRIVED ─────────────────── end
```

---

## ✅ Key Features

- **360° LiDAR obstacle detection** — knows what's around the rover at all times
- **DeepSORT person tracking** — locks onto the user and never confuses them with someone else
- **Real-time A\* path replanning** — if something blocks the way, it finds a new route
- **Spatial voice announcements** — tells the user what's nearby and where (*"person on your left"*)
- **Stair detection** — both upward risers (seen by LiDAR) and downward drops (ToF sensor)
- **Independent ESP32 goggles** — haptic + audio alerts even if the rover's main system fails
- **Graceful WiFi failure** — if the camera stream drops, LiDAR + A\* keep the rover navigating
- **User-aware speed control** — rover speeds up or slows down based on how far behind the user is

---

## 📁 Project Structure

```
EchoSight/
│
├── src/
│   ├── main_controller.py      # Central state machine — ties everything together
│   ├── lidar_node.py           # RPLidar interface and raw scan processor
│   ├── motor_control.py        # L298N GPIO interfacing and PWM control
│   ├── camera_stream.py        # DroidCam MJPEG stream reader
│   ├── yolo_detector.py        # YOLOv8n object detection + spatial audio cues
│   ├── deepsort_tracker.py     # DeepSORT person ID tracking
│   ├── person_tracker.py       # LiDAR-based user position tracking (rear arc)
│   ├── astar_planner.py        # Custom A* pathfinder on live occupancy grid
│   ├── stair_detector.py       # Downward drop and upward stair detection
│   └── tts_speaker.py          # pyttsx3 text-to-speech with dedup logic
│
├── goggles/
│   └── goggles.ino             # ESP32 Arduino firmware for user-worn goggles
│
├── models/
│   └── yolov8n.pt              # YOLOv8 weights — add locally (not committed)
│
├── tests/
│   ├── test_lidar.py           # Standalone LiDAR scan test
│   ├── test_motors.py          # Motor direction and speed test
│   └── test_camera.py          # DroidCam stream connection test
│
├── media/
│   ├── photos/                 # Photos of the rover and goggles
│   └── videos/                 # Demo recordings and simulations
│
├── requirements.txt
└── README.md
```

---

## 🚀 Getting Started

### Prerequisites

- Raspberry Pi 4 running Raspberry Pi OS 64-bit (Bookworm)
- Python 3.12
- RPLidar A2 connected via USB
- DroidCam (or IP Webcam) running on a phone connected to the same WiFi
- L298N motor driver wired up (see wiring section)

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/EchoSight.git
cd EchoSight
```

### 2. Set up the Python environment

```bash
sudo apt install -y python3-venv python3-dev build-essential \
    libopencv-dev espeak portaudio19-dev

python3 -m venv venv --system-site-packages
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Add LIDAR permissions

```bash
sudo usermod -a -G dialout $USER
# Log out and back in after this
```

### 4. Run individual tests first

```bash
python3 tests/test_lidar.py    # Confirm LIDAR is scanning
python3 tests/test_motors.py   # Confirm wheels spin correctly (keep wheels off ground)
python3 tests/test_camera.py   # Confirm DroidCam feed is reachable
```

### 5. Run the full system

```bash
python3 src/main_controller.py 4.0 0.0
# Arguments: goal X and Y in metres from the rover's starting position
```

You should hear *"Path planning"* → *"Following you. Walk forward."* — then start walking behind the rover.

---

## 🗺️ GPIO Wiring Reference

| L298N Pin | Raspberry Pi GPIO | Function |
|-----------|------------------|----------|
| ENA | GPIO 18 | PWM — left motor speed |
| IN1 | GPIO 23 | Left motor direction A |
| IN2 | GPIO 24 | Left motor direction B |
| IN3 | GPIO 25 | Right motor direction A |
| IN4 | GPIO 8 | Right motor direction B |
| ENB | GPIO 13 | PWM — right motor speed |
| GND | GND (Pin 6) | Common ground |

> **Important:** Never power the Pi through the L298N's 5V output. Always use a dedicated 5V 3A USB-C supply for the Pi.

> *(Add a wiring diagram photo or schematic here)*

---

## 👥 Team — AI-4B, FAST NUCES Islamabad

This project was built by a team of five over several weeks of hardware debugging, late nights, and a lot of burnt patience (and one motor driver).

- **Ahmed Raza** 
- **Muhammad Shaheed Khan** 
- **Abuzar Ali** 
- **Abdul Sammad**
- **Faizan Ahmad**

---


## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---

<div align="center">
  <i>Built with purpose. EchoSight — because independence shouldn't require perfect vision.</i>
</div>
