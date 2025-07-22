
# 🚨 Graph-RAG: Fraud Detection with Neo4j and LLM

A graph-based Retrieval-Augmented Generation (RAG) system for **fraud detection**, built using **Neo4j**, **Ollama (LLaMA 3)**, and **Streamlit**. The system models 1.4M+ transactions, supports multi-hop reasoning, visualizes fraud networks, and integrates an LLM for intelligent decision-making with reduced hallucinations.

---

## 🔍 Overview

Traditional fraud detection struggles to capture complex relationships across transactions, devices, IPs, and payment methods. This project introduces a **Graph-RAG** approach to enhance reasoning by:

- **Modeling relationships** using Neo4j (customer ↔ transaction ↔ device ↔ IP)
- **Visualizing transaction graphs** with PyVis + Streamlit
- **Generating fraud predictions** using **Ollama (LLaMA 3)** with LangChain-style prompts
- **Reducing hallucinations** compared to standard RAGs by contextual grounding in the graph

---

## 💡 Key Features

- 📊 **Graph Inference on 1.4M records**, 16 features, 300K+ nodes
- 🔁 Multi-hop graph traversal across fraud-relevant entities
- 🧠 Integrated **Ollama LLaMA 3** for explainable, structured LLM outputs
- ✅ Achieved **34% reduction in hallucinations** vs baseline RAG
- ⚡ Built real-time fraud analysis interface using **Streamlit**

---

## 🧰 Tech Stack

| Component      | Tool/Library        |
|----------------|---------------------|
| Graph Database | Neo4j               |
| LLM            | Ollama (LLaMA 3)    |
| UI             | Streamlit           |
| Visualization  | PyVis               |
| Prompt Engine  | LangChain-style     |
| Language       | Python              |

---

## 🚀 Setup Guide

### 1️⃣ Clone Repository

```bash
git clone https://github.com/yourusername/graph-rag-fraud.git
cd graph-rag-fraud
pip install -r requirements.txt

## Features

- Create a RAG from PDFs
- Graph visulation through Neo4j Browser
- All data are stored locally, supporting llama.cpp and Ollama local LLM

## Installation

 clone this project and install dependencies
 you need to install Neo4j. Download [Neo4j Desktop](https://neo4j.com/download/) or Mac can install with homebrew
 
 brew install --cask neo4j
 ```
 1. Launch Neo4j Desktop, create a New Project and add a new Graph DBMS.
 1. Enter the password into the [config.ini](./config.ini) - Neo4j - password. Then click on the Graph DBMS created in the last step and install [APOC plugin](https://github.com/neo4j/apoc).
 1. Start the Graph DBMS.

<big>**Step3**</big> (optional) Set up [Ollama](https://ollama.com) or [llama.cpp](https://github.com/ggerganov/llama.cpp) to use local LLM.
 - For Ollama, download the app [here](https://ollama.com), run Ollama and then
 ```
 ollama run llama3
 ```
 *P.S. hermers-2-pro has a better sepport to function calling than original llama3.*
 - For llama.cpp, follow the instruction [here](https://github.com/ggerganov/llama.cpp) to build and run llama.cpp server.

