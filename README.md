# 📺 select-freeboxos-win v2.0.0

> 📡 Turn your Freebox into an automated recording system
> 🎯 Automatically schedule TV recordings via Freebox OS

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![Platform](https://img.shields.io/badge/Platform-Windows-blue)
![Architecture](https://img.shields.io/badge/Arch-x86-orange)
![Status](https://img.shields.io/badge/Status-Active-success)
![Self-hosted](https://img.shields.io/badge/Self--Hosted-Yes-blueviolet)
![Dependency](https://img.shields.io/badge/Requires-Freebox%20OS-lightgrey)

---

## 🍿 How TV Select works

TV Select turns TV into a **personal discovery engine**.

You define what you care about:

* a documentary about wine 🍷
* a history episode 🏛️
* a space report 🚀
* that rare movie you couldn’t find anywhere 🎬
* a tennis documentary your son will love 🎾

Then the system works for you:

1. 🔍 Your searches are analyzed
2. 🧠 TV programs are continuously scanned
3. 🎯 When a match is found:

   * 📧 You receive a notification
   * 📼 A recording is triggered automatically

👉 No manual searching. No scheduling.

---

## 📖 TV Select Ecosystem

This project is part of the **TV Select ecosystem**.

👉 Overview & setup guide:

[![TV Select Ecosystem](https://img.shields.io/badge/TV%20Select-Ecosystem-blue)](https://github.com/tv-select)

## 📡 About select-freeboxos-win

select-freeboxos-win does **not record videos directly**.

👉 Instead, it:

- connects to **Freebox OS**
- automatically **schedules recordings**
- lets the Freebox handle the recording

---

## ⚡ Key features

- 📡 Automatic recording scheduling via Freebox OS
- 💾 Record directly on Freebox internal or USB storage
- 🧠 Uses MEDIA-select API for program detection
- 🤖 Browser automation (Selenium)
- 🔄 Runs automatically at Windows startup
- ⚙️ Fully automated once configured

---

## 🧩 How it works

Search → Match → Schedule (Freebox OS) → Record → Watch

---

## 🏠 Freebox OS integration

This application uses the **recording feature of Freebox OS**.

- Recordings are stored on the Freebox
- No local video storage required on your PC

👉 Important:

- Your PC must be started regularly (at least once every 7 days)
- TV program data is available up to 7 days ahead

💡 For a fully automated setup, consider using a dedicated machine (SBC / VM).

---

## 📁 Output

Videos are stored directly on your Freebox.

Accessible via:

- Freebox OS interface
- Network shares (SMB)
- Connected devices (TV, media players)

---

## ⚡ Installation

### Requirements

- Windows 10 / 11
- Python 3.9+
- Freebox OS (version ≥ 4.7)
- Account on https://www.media-select.fr

---

### Install

Download and extract the project:

select-freeboxos-win-master.zip

---

### Setup

Open PowerShell as administrator and run:

cd "$HOME\Downloads\select-freeboxos-win-master\select-freeboxos-win-master"

Set-ExecutionPolicy Bypass -Scope Process ; ./setup.ps1

---

### Configure

Run:

C:\Venvs\select_freeboxos\Scripts\python.exe C:\Apps\select_freeboxos\install.py

Then:

- Enter your Freebox OS admin password
- Enter your MEDIA-select credentials

---

## 🔐 Security

This application interacts with **Freebox OS using your admin credentials**.

### 🟢 Local usage (recommended)

- Runs on a device within your home network
- Connects directly to your Freebox using local addresses (e.g. `192.168.1.254`, `mafreebox.freebox.fr`)
- HTTP is allowed only in this context

### 🟡 Remote usage (secure)

- Remote access is possible **only with HTTPS enabled**
- Connections over HTTP outside the local network are **blocked automatically**
- A warning is displayed when a remote connection is detected

### 🔴 Unsafe configurations

- Remote HTTP connections are **blocked by the application**
- This prevents exposure of your Freebox admin credentials

---

💡 By default, the application enforces security rules based on the network context.

## ⏳ What to expect

- ❌ No immediate results
- ⏳ Wait for matches
- 🎯 Recordings are scheduled automatically
- 📼 Videos are recorded by the Freebox

---

## 🧩 Architecture

Search → Match → Freebox OS → Schedule → Record → Watch

---

## 🤔 When should you use select-freeboxos-win?

Use this version if:

- you use a Windows PC
- you want a simple setup without dedicated hardware
- you start your PC regularly (at least weekly)

---

## ⚠️ Limitations

- Requires Freebox OS
- Requires Windows session startup
- Requires periodic usage (at least once every 7 days)
- Relies on browser automation (Selenium)

---

## ⭐ Support

If you like this project:

- ⭐ Star it
- 🔁 Share it
- 🧠 Use it

---

## ⚠️ Disclaimer

For personal use only.
