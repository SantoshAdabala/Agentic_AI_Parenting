# Parenting Agent
An AI-driven, modular Parenting Agent built with Google’s Agent Development Kit (ADK) and FatSecret integration to answer all your parenting, nutrition, and basic medical questions—right from your command line.
## Features
### Root Conversational Agent
Delegates incoming queries to specialized sub-agents or tools:
- Parenting Analyst: Child behavior, development milestones, and parenting tips.
- Nutrition Meal Planner: Calories, macros, and custom meal plans powered by FatSecret’s Nutrition API.
- Medical Advice Assistant: Basic pediatric medical guidance (for non-emergency questions).
- Google Search & Data Fetch: Falls back to web search or your own fetch_parenting_data tool for anything else.
- Current Time Tool: Returns local date and time on demand.
### Stateful Sessions
- Uses an in-memory session service to remember user names and preferences across turns.
### Extensible Architecture
- Easily add new sub-agents or tools by registering them with the root agent.
## Architecture
<img width="739" alt="Screenshot 2025-05-15 at 12 23 47 PM" src="https://github.com/user-attachments/assets/2ea7c7ee-c045-4b94-b930-4fee7c0de543" />

1. Runner wires the agent and session service, processing input/output events.
2. root_agent contains your delegation instructions, tool list, and model selection.
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
# 1. Clone the repo
git clone https://github.com/SantoshAdabala/Agentic_AI_Parenting.git
cd Agentic_AI_Parenting

# 2. Create & activate a virtual environment
python3.11 -m venv env
source env/bin/activate

# 3. Install dependencies
pip install --upgrade pip
pip install -r requirements.txt
```
## Configurations 
Create a .env file in the repo root with your credentials:
```bash
# .env
GOOGLE_ADK_API_KEY=your_google_adk_api_key_here
FATSECRET_KEY=your_fatsecret_api_key_here
FATSECRET_SECRET=your_fatsecret_api_secret_here
```
The code uses python-dotenv to load these at runtime.

## Usage

Launch a stateful session and test your agent:
```bash
python stateful_session.py
```
You should see output like:
```bash
CREATED NEW SESSION:
    Session ID: 123e4567-e89b-12d3-a456-426614174000
Agent: Hello! What’s your name?
# … then try asking:
# “What foods help a 2-year-old grow strong?”
# “How can I soothe a teething baby?”
```
## Project Structure 
```bash
Agentic_AI_Parenting/
└── basic_agent/
│   └── .env
└── conversational_agent /
    ├── agent.py           # root_agent definition
    ├── .env
    ├── __init__.py
    ├── stateful_session.py
    ├── tools/
    │   └── tools.py      # get_current_time, google_search, fetch_parenting_data, etc.
    │   └── __init__.py
    └── sub_agents/
        ├── parenting_analyst/
        │   └── agent.py
        ├── nutrition_meal_planning/
        │   └── agent.py
        │   └── __init__.py
        └── medical_advice_assistance/
            └── agent.py
```
