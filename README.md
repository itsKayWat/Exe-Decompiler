# ⚙️ Universal Executable Decompiler (Exe-Decompiler)

[![KayWat Web Tools](https://img.shields.io/badge/KayWat-Ecosystem-007ACC?style=for-the-badge&logo=github)](https://kaywat.codes/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)
[![Platform: Windows](https://img.shields.io/badge/Platform-Windows_10%2F11-blue?style=for-the-badge&logo=windows)](https://microsoft.com/windows)
[![Python: 3.7+](https://img.shields.io/badge/Python-3.7%2B-green?style=for-the-badge&logo=python)](https://python.org)

> **Universal Windows & Electron Executable Reverse Engineering Suite**  
> *A high-performance security research tool for binary analysis, resource extraction, and ASAR archive decompilation.*

---

## 🌟 Overview & Capabilities

**Exe-Decompiler** is a specialized analysis framework designed for security researchers, developers, and malware analysts. It provides automated detection, PE (Portable Executable) inspection, resource extraction, and Electron app decompilation.

### Key Features

- 🔍 **Automated Binary Classification**: Instantly detects whether a target executable is an **Electron** app, a **.NET** assembly, or a **Native Windows PE** binary.
- 📦 **ASAR Archive Unpacker**: Extracts internal source files and assets from Electron application `.asar` bundles.
- 🛠️ **PE Structural Analysis**: Direct extraction of icons, strings, bitmaps, embedded executables, and manifest XMLs.
- 🗺️ **Source Map Inspector**: Identifies and parses JavaScript source maps within minified web bundles for auditability.
- 🖥️ **Modern Desktop GUI**: Built-in graphical launcher (`run_gui.py`) and command-line interfaces (`launcher.py`).

---

## 🚀 Getting Started

### System Prerequisites
- **Operating System**: Windows 10 / Windows 11
- **Python Runtime**: Python 3.7 or higher
- **Optional**: Node.js (required for full Electron ASAR unpacking)

### Installation & Setup

1. **Clone the Public Showcase**:
   ```bash
   git clone https://github.com/itsKayWat/Exe-Decompiler.git
   cd Exe-Decompiler
   ```

2. **Install Required Tooling**:
   ```bash
   python requirements.py
   ```

3. **Launch the Application**:
   - Graphical User Interface:
     ```bash
     python run_gui.py
     ```
   - Terminal CLI Launcher:
     ```bash
     python launcher.py
     ```

---

## 📖 Usage Guide

### 1️⃣ Analyzing Native Windows Executables
1. Select any target `.exe` file in the main interface.
2. Click **Analyze PE File** to inspect PE headers, sections, and import tables.
3. Click **Extract PE Resources** to dump embedded icons, string tables, manifests, and binaries into the output folder.

### 2️⃣ Decompiling Electron Applications
1. Select an Electron-based application launcher or bundle.
2. Click **Extract ASAR** to unpack JavaScript resources and app assets.
3. Use **Analyze Source Maps** to map minified frontend code back to original source structures.

---

## ⚖️ Legal & Privacy Disclaimer

*This project is published for educational, security auditing, and interoperability research purposes. Users are responsible for ensuring compliance with applicable copyright laws and software terms of service.*

---

© 2026 **[KayWat Architecture Suite](https://kaywat.codes/)**. All rights reserved.
