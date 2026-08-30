# ⚡ Universal Executable Decompiler (Exe-Decompiler)

[![KayWat Ecosystem](https://img.shields.io/badge/KayWat-Ecosystem-0088cc?style=for-the-badge&logo=github)](https://decompiler.kaywat.codes/)
[![Ocean Teal UI](https://img.shields.io/badge/Ocean_Teal-Security_Portal-38c0ff?style=for-the-badge)](https://decompiler.kaywat.codes/)
[![License: Proprietary EULA](https://img.shields.io/badge/License-Proprietary_EULA-red.svg?style=for-the-badge)](LICENSE.txt)
[![Platform: Windows](https://img.shields.io/badge/Platform-Windows_10%2F11-blue?style=for-the-badge&logo=windows)](https://microsoft.com/windows)

> **Universal Windows & Electron Executable Reverse Engineering Platform**  
> *A high-performance binary inspection tool, PE resource extractor, PyInstaller unpacker, and Electron ASAR archive decompilation suite.*

---

## 🌐 Official Web Portal & Downloads

Visit our live web platform: **[https://decompiler.kaywat.codes/](https://decompiler.kaywat.codes/)**

### 📥 Download Options:

1. ⚡ **Official Windows Setup Installer (`Exe-Decompiler-Setup.exe`)**:
   - Download directly via the **[Cloudflare CDN Installer Stream](https://exe-decompiler-downloader.gvtechhub.workers.dev/download)** or from **[GitHub Releases](https://github.com/itsKayWat/Exe-Decompiler_dev/releases)**.

2. 🚀 **Direct Standalone Executable (`Exe-Decompiler.exe`)**:
   - Download the portable executable directly without installer setup:
   - **[Direct Download (.exe) via Google Drive](https://drive.google.com/uc?export=download&id=1gXamvoHcV9vG0WPeiDS5ol89PKijLG5m)**

---

## 🔥 Recent Updates & Milestones (v1.1.6-beta)

- 📡 **Real-Time Job Monitoring & Event-Driven Streaming (`v1.1.6-beta`)**: Low-latency WebSocket job progress streaming via Redis pub/sub, sequence counter deduplication, automated backoff reconnect, visibility-aware HTTP polling fallback, granular cancellation/retry endpoints, attempt history tracking, and stalled worker recovery.
- 🔒 **Private Paid Results Explorer (`results.html`)**: Manifest-driven, user-scoped results viewer featuring section tabs for PE Headers, PE Sections, Import Dependencies, String Inventory, PE Resources, Electron ASAR source trees, PyInstaller bytecode, Source Map restoration, Paginated Extracted Files Browser with text code preview, line numbers, copy controls, report generation, and 15-minute retention download packages.
- 🔬 **Public Free Decompiler Explorer (`explorer.html`)**: Dogbolt-inspired multi-engine code inspection interface featuring side-by-side viewports for PE Headers, Disassembly, ASAR, PyInstaller, Strings, and Imports with 1:1 synchronized line-number gutters, per-column copy controls, real-time waiting indicators, and deep-linkable URL sessions (`?analysisId=...`).
- 🛡️ **Cryptographic Free-Tier Rate Limiting**: Keyed HMAC-SHA256 visitor fingerprinting with dedicated `RATE_LIMIT_SECRET` to prevent rate-limit manipulation while protecting free engine queues.
- 🎨 **Ocean Teal Security Portal**: Overhauled web portal featuring a clean layout tuned for instant binary sample submission and research.
- 🧱 **Hardened Production SaaS Infrastructure**: Upgraded backend architecture utilizing FastAPI web services, PostgreSQL database persistence, Redis job queues, isolated background workers, and private R2 object storage.

---

## 🌟 Core Capabilities & Extraction Engines

- 🔍 **Automated Binary Classification**: Instantly identifies target binary frameworks—including **Electron (ASAR)**, **PyInstaller**, **.NET Assemblies**, and **Native Windows PE**.
- 📦 **ASAR Archive Unpacker**: Extracts internal JavaScript source bundles, configuration files, and assets from Electron application `.asar` packages.
- 🐍 **PyInstaller De-Archiver**: Extracts compiled Python bytecode (`.pyc`) and embedded DLL dependencies from PyInstaller executables.
- 🛠️ **PE Header & Resource Dumper**: Extracts embedded icons, string tables, bitmaps, manifests, and section structures directly from PE headers.
- 🗺️ **Source Map Inspector**: Discovers and decodes embedded JavaScript/TypeScript source maps to reconstruct original un-minified source code.
- 🛡️ **Hardened C++ Engine & Desktop GUI**: Features a custom dark-themed Windows desktop application with dependency verification, interactive file trees, and built-in GitHub issue tracking.

---

## 🏗️ Architecture Overview

```mermaid
flowchart TD
    A["Landing Page"] --> B["Free Explorer"]
    B --> C["Free API"]
    C --> D["Free Queue"]
    D --> E["Temporary Analysis"]

    F["Paid Dashboard"] --> G["FastAPI Gateway"]
    G --> H["BetterBase Auth"]
    G --> I["Stripe Entitlements"]
    G --> J["PostgreSQL Jobs"]
    G --> K["Paid Queue"]
    K --> L["Extraction Worker"]
    L --> M["Private R2 Results"]
```

### 🔄 Job Lifecycle & State Machine

```mermaid
stateDiagram-v2
    [*] --> queued
    queued --> processing
    queued --> cancelled
    processing --> packaging
    processing --> failed
    processing --> cancelled
    packaging --> complete
    packaging --> failed
    complete --> deleted
    failed --> queued: Retry
    cancelled --> queued: Retry
```

---

## 🗺️ Development Roadmap

- [x] **v1.1.1-beta**: Paid Workspace Shell & Authentication Paywall Gating.
- [x] **v1.1.2-beta**: Persistent Job Infrastructure, PostgreSQL schema, Redis RQ queue & private storage abstraction.
- [x] **v1.1.3-beta**: Production Hardening, Stripe webhook idempotency, CORS, and health checks.
- [x] **v1.1.4-beta**: Public Free Explorer (`explorer.html`), side-by-side inspection viewports, and free vs. paid results separation.
- [x] **v1.1.5-beta**: Paid Results Explorer (`results.html`) with interactive source-map viewer and paginated file browser.
- [x] **v1.1.6-beta**: Real-time jobs, WebSocket status streaming, automatic reconnect backoff, polling fallback, cancel/retry endpoints, and stalled worker recovery.
- [ ] **v1.1.7-beta**: Dashboard history, account UX, search, filtering, and usage quotas.
- [ ] **v1.2.0-beta**: Ghidra Cloud Worker integration (headless container, CPU/memory caps, decompiled C-like browser).
- [ ] **v1.3.0-beta**: AI Reverse Engineering Assistant (LLM-powered threat summaries, variable renaming, function explanation).

---

## ⚖️ Legal & Privacy Disclaimer

*This software and platform are provided for educational, security auditing, and interoperability research purposes. Users are responsible for ensuring compliance with applicable copyright laws, license agreements, and software terms of service.*

---

## 🏢 Maintenance & Security Policy

All roadmap planning, internal task tracking, and proprietary backend source code are maintained in private development repositories. Only sanitized ecosystem documentation, security notices, installer binaries, and public interface specifications are published to this public release repository.

---

© 2026 **[Exe-Decompiler](https://decompiler.kaywat.codes/)**. A **[KayWat Codes](https://kaywat.codes/)** Production. All rights reserved.
