# Geopolitical Policy Chatbot

A sophisticated AI-powered chatbot designed for exploring **geopolitical policy, international trade, and sanctions regulations**. This project integrates **LLM-based natural language processing**, official datasets, and a **web-based interface** for interactive queries, while enforcing strict safety and compliance checks.  

The chatbot can respond to complex policy questions, retrieve information from **OFAC sanctions lists** and **WTO trade datasets**, and guide users on international trade rules, embargoes, and export controls.

---

## Key Features

- **LLM-Powered Responses**: Uses a large language model to generate nuanced, context-aware answers.  
- **Dataset Integration**: Query official CSV datasets such as:  
  - **OFAC Specially Designated Nationals (SDN) List** – track individuals, entities, and addresses under U.S. sanctions.  
  - **WTO Trade Data** – access trade-weighted MFN tariffs and bilateral services statistics.  
- **Safety & Compliance Checks**: Automatically blocks unsafe, illegal, or sensitive queries.  
- **Interactive Web Frontend**: Simple and aesthetic HTML/CSS interface for real-time chat.  
- **FastAPI Backend**: Lightweight API for scalable deployment and future integrations.  
- **Extensible Design**: Easy to add new datasets, prompts, or LLM providers.  

---

## Demo

- Run locally and open the web interface at `http://127.0.0.1:8000` to ask questions interactively.  
- Supports **automatic blocking of dangerous queries** and provides structured answers with **educational disclaimers**.  

---

Example Queries

“What are the current OFAC sanctions on Cuba?”
“Explain the difference between MFN tariffs and preferential tariffs.”
“How do EU sectoral sanctions work?”
“What impact do trade tariffs have on developing countries?”

The bot automatically provides educational disclaimers, references relevant datasets, and blocks dangerous or illegal queries.

---

Technology Stack

Backend: Python, FastAPI
Frontend: HTML, CSS, JavaScript
Data Handling: Pandas for CSV lookups
LLM Integration: OpenAI API (or any compatible LLM)

---

## Installation & Setup

1. **Clone the repository**

```bash
git clone https://github.com/<your-username>/geopolitical-policy-chatbot.git
cd geopolitical-policy-chatbot
