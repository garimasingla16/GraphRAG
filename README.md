
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
