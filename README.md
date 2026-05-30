# Parenting Agent

An AI-driven, modular Parenting Agent built with Google's Agent Development Kit (ADK) and FatSecret integration to answer all your parenting, nutrition, and basic medical questions - right from your command line.

---

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![Google ADK](https://img.shields.io/badge/Google%20ADK-0.3.0-4285F4?style=flat-square&logo=google&logoColor=white)](https://google.github.io/adk-docs)
[![Gemini](https://img.shields.io/badge/Gemini-generativeai-8B5CF6?style=flat-square&logo=googlegemini&logoColor=white)](https://ai.google.dev)
[![LiteLLM](https://img.shields.io/badge/LiteLLM-1.66-0EA5E9?style=flat-square)](https://litellm.ai)
[![FatSecret](https://img.shields.io/badge/FatSecret-Nutrition%20API-F97316?style=flat-square)](https://platform.fatsecret.com)

[![Stars](https://img.shields.io/github/stars/SantoshAdabala/Agentic_AI_Parenting?style=flat-square&color=FBBF24)](https://github.com/SantoshAdabala/Agentic_AI_Parenting/stargazers)
[![Last Commit](https://img.shields.io/github/last-commit/SantoshAdabala/Agentic_AI_Parenting?style=flat-square&color=64748B)](https://github.com/SantoshAdabala/Agentic_AI_Parenting/commits/main)

---

## Features

### Root Conversational Agent
Delegates incoming queries to specialized sub-agents or tools:
- **Parenting Analyst** - Child behavior, development milestones, and parenting tips.
- **Nutrition Meal Planner** - Calories, macros, and custom meal plans powered by FatSecret's Nutrition API.
- **Medical Advice Assistant** - Basic pediatric medical guidance (for non-emergency questions).
- **Google Search & Data Fetch** - Falls back to web search or your own fetch_parenting_data tool for anything else.
- **Current Time Tool** - Returns local date and time on demand.

### Stateful Sessions
Uses an in-memory session service to remember user names and preferences across turns.

### Extensible Architecture
Easily add new sub-agents or tools by registering them with the root agent.

## Architecture

<img width="739" alt="Screenshot 2025-05-15 at 12 23 47 PM" src="https://github.com/user-attachments/assets/2ea7c7ee-c045-4b94-b930-4fee7c0de543" />

1. Runner wires the agent and session service, processing input/output events.
2. `root_agent` contains your delegation instructions, tool list, and model selection.
3. Sub-agents implement domain-specific logic (API calls, parsing, response formatting).

---

## Getting Started

### Prerequisites

- **Python 3.11+**
- **Git**
- A **Google Cloud** project with ADK access (service account or API key)
- A **FatSecret** developer account (API key + secret)

### Installation

```bash
git clone https://github.com/SantoshAdabala/Agentic_AI_Parenting.git
cd Agentic_AI_Parenting
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Fill in GOOGLE_API_KEY, FATSECRET_CLIENT_ID, FATSECRET_CLIENT_SECRET
```

### Run

```bash
python basic_agent/agent.py
```
