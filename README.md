# **AI‑Assisted Support Chatbot (ASC)**

---

## **What This Is:**
<u></u>

This repository contains the **AI‑Assisted Support Chatbot (ASC)**, a Python‑based web application designed to support Tier 1 technical support agents during live customer calls. The system provides structured, step‑by‑step troubleshooting guidance using documented knowledge to help agents resolve common issues or escalate them cleanly when resolution is not possible.

The ASC is intended as an **internal decision‑support tool**, not an end‑user chatbot. Its goal is to reduce unnecessary escalations, improve first‑contact resolution, and ensure consistent support outcomes in high‑turnover environments.

---

## **What’s Inside:**
<u></u>

- **app/** – Flask application source code  
  - Core session engine and reasoning logic  
  - State‑managed troubleshooting flows  
  - Escalation handling and session completion logic
- **app/templates/** – HTML templates for the web interface  
- **static/** – Basic CSS for layout and presentation  
- **data/** – JSON files defining knowledge articles, troubleshooting steps, and flows  
- **README.md**  
- **.gitignore**

---

## **Key Features:**
<u></u>

- Guided, step‑by‑step troubleshooting flows  
- Deterministic session state management  
- Explicit resolution and escalation paths  
- Clean, minimal web interface for live‑call use  
- Structured escalation summaries for Tier 2 handoff  
- Designed for clarity, predictability, and maintainability  

---

## **How to Run:**
<u></u>

1. Ensure **Python 3** is installed.
2. Create and activate a virtual environment.
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
4. Run the Flask application:
   ```
   python -m app.app
   ```
5. Open a browser and navigate to:
   ```
   http://127.0.0.1:5000/session
   ```

---

## **Created By:**
<u></u>

**Jared Hutchins**
