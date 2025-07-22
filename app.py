# 📦 Graph RAG Fraud Detection App: Final Updated Version

import streamlit as st
from neo4j import GraphDatabase
import requests
import json
import os
from pyvis.network import Network
import streamlit.components.v1 as components

# ---------------------------
# Neo4j Config
# ---------------------------
NEO4J_URI = "bolt://localhost:7687"
NEO4J_USERNAME = "neo4j"
NEO4J_PASSWORD = "password"  # Update this

# ---------------------------
# Neo4j DB Access Class
# ---------------------------
class Neo4jDB:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def get_transaction_graph(self, tx_id):
        query = """
        MATCH (t:Transaction {id: $tx_id})
        OPTIONAL MATCH (c:Customer)-[:MADE]->(t)
        OPTIONAL MATCH (t)-[:USED]->(pm:PaymentMethod)
        OPTIONAL MATCH (t)-[:PRODUCT_TYPE]->(pc:ProductCategory)
        OPTIONAL MATCH (t)-[:SHIPPED_TO]->(sa:ShippingAddress)
        OPTIONAL MATCH (t)-[:BILLED_TO]->(ba:BillingAddress)
        OPTIONAL MATCH (t)-[:INITIATED_BY]->(d:Device)
        OPTIONAL MATCH (t)-[:FROM_IP]->(ip:IPAddress)
        OPTIONAL MATCH (c)-[:LOCATED_IN]->(loc:Location)
        RETURN t, c, pm, pc, sa, ba, d, ip, loc
        """
        with self.driver.session() as session:
            result = session.run(query, tx_id=tx_id)
            graph = {"nodes": [], "edges": [], "props": {}, "category": None}
            seen = set()
            for record in result:
                t = record['t']
                graph['props'] = dict(t)
                graph['nodes'].append(("Transaction", dict(t)))
                seen.add(("Transaction", dict(t)['id']))

                connections = [
                    ('Customer', 'c', 'id', 'MADE'),
                    ('PaymentMethod', 'pm', 'method', 'USED'),
                    ('ProductCategory', 'pc', 'name', 'PRODUCT_TYPE'),
                    ('ShippingAddress', 'sa', 'address', 'SHIPPED_TO'),
                    ('BillingAddress', 'ba', 'address', 'BILLED_TO'),
                    ('Device', 'd', 'type', 'INITIATED_BY'),
                    ('IPAddress', 'ip', 'ip', 'FROM_IP'),
                    ('Location', 'loc', 'name', 'LOCATED_IN')
                ]

                for label, key, prop, rel in connections:
                    node = record.get(key)
                    if node:
                        node_props = dict(node)
                        node_id = node_props.get(prop)
                        node_tuple = (label, node_id)
                        if node_tuple not in seen:
                            graph['nodes'].append((label, node_props))
                            seen.add(node_tuple)
                        if label == 'Location':
                            if record['c']:
                                graph['edges'].append((dict(record['c'])['id'], node_id, rel))
                        elif label == 'Customer':
                            graph['edges'].append((node_id, dict(t)['id'], rel))
                        else:
                            graph['edges'].append((dict(t)['id'], node_id, rel))

                if record['pc']:
                    graph['category'] = dict(record['pc'])['name']
            return graph

    def get_avg_amounts_by_category(self):
        query = """
        MATCH (t:Transaction)-[:PRODUCT_TYPE]->(pc:ProductCategory)
        RETURN pc.name AS category, avg(t.amount) AS avg_amount
        """
        with self.driver.session() as session:
            result = session.run(query)
            return {r["category"]: round(r["avg_amount"], 2) for r in result}


# ---------------------------
# Graph Visualization (pyvis)
# ---------------------------
def show_graph(nodes, edges):
    net = Network(height='500px', width='100%', bgcolor='#ffffff', font_color='black')
    net.barnes_hut(gravity=-20000, central_gravity=0.3, spring_length=300, spring_strength=0.05)

    label_color_map = {
        "Transaction": "orange",
        "Customer": "lightgreen",
        "PaymentMethod": "yellow",
        "ProductCategory": "pink",
        "ShippingAddress": "gray",
        "BillingAddress": "lightblue",
        "Device": "lightgray",
        "IPAddress": "purple",
        "Location": "cyan"
    }

    added_ids = set()

    for label, props in nodes:
        node_id = props.get("id") or props.get("method") or props.get("name") or props.get("address") or props.get("ip") or props.get("type")
        if node_id is None or node_id in added_ids:
            continue
        added_ids.add(node_id)
        node_label = next(iter(props.values()), label)  # Use actual value instead of label if exists
        title = f"{label}: {node_label}\n" + "\n".join(f"{k}: {v}" for k, v in props.items())
        color = label_color_map.get(label, "gray")
        net.add_node(node_id, label=str(node_label), title=title, color=color)

    for src, tgt, rel in edges:
        if src in added_ids and tgt in added_ids:
            net.add_edge(src, tgt, label=rel)

    net.save_graph("graph.html")
    components.html(open("graph.html", "r", encoding="utf-8").read(), height=550)


# ---------------------------
# Ollama LLM Call
# ---------------------------
def call_ollama(prompt):
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": "llama3", "prompt": prompt, "stream": False}
        )
        response.raise_for_status()
        result = response.json()
        return result.get("response"), None
    except Exception as e:
        return None, str(e)

# ---------------------------
# Streamlit UI
# ---------------------------
st.set_page_config(page_title="Graph RAG Fraud Detector", layout="wide")
st.title("📊 Graph RAG: Fraud Detection with Neo4j + Ollama")
query_id = st.text_input("Enter Transaction ID", "4e707452-7c8a-4cbd-b0c1-2aeaa35c5e88")

if st.button("Analyze Transaction"):
    db = Neo4jDB(NEO4J_URI, NEO4J_USERNAME, NEO4J_PASSWORD)
    try:
        st.info("Fetching graph data from Neo4j...")
        graph_data = db.get_transaction_graph(query_id)

        if graph_data["nodes"]:
            st.success("Transaction node found.")
            st.subheader("Graph View")
            show_graph(graph_data["nodes"], graph_data["edges"])

            st.subheader("Transaction Properties")
            for k, v in graph_data['props'].items():
                st.write(f"**{k}:** {v}")

            props_no_label = {k: v for k, v in graph_data['props'].items() if k != 'is_fraud'}
            category_avgs = db.get_avg_amounts_by_category()

            prompt = f"""
            You are a financial fraud analyst AI.
            
            Transaction Details:
            {json.dumps(props_no_label, indent=2)}

            Category Average Amounts:
            {json.dumps(category_avgs, indent=2)}

            Instructions:
            - Classify a transaction as FRAUDULENT only if:
              a) Its amount exceeds 2× the average of its product category,
              AND
              b) At least one more red flag exists: mismatched addresses, reused IP/device, suspicious hour, or new customer.
            - If only one minor anomaly is present, classify as NOT_FRAUDULENT.

            Return the result as JSON:
            {{
              "prediction": "FRAUDULENT" or "NOT_FRAUDULENT",
              "analysis": "concise reasoning"
            }}
            """

            st.info("Calling Ollama (LLaMA 3) for LLM-based fraud analysis...")
            full_response, err = call_ollama(prompt)

            if err:
                st.error(f"Ollama Error: {err}")
            else:
                st.success("Ollama Response:")
                st.code(full_response, language="json")
                truth = graph_data['props'].get('is_fraud')
                if truth is not None:
                    st.markdown(f"**Actual (Ground Truth):** `{truth}`")
    except Exception as e:
        st.exception(e)
    finally:
        db.close()
