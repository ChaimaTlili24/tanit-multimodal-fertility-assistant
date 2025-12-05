# GraphRAG Index (Prototype)

This folder represents the place where a real Microsoft GraphRAG index
would live in a production system.

In this prototype:

- We do **not** build or load a full GraphRAG graph (for simplicity and
  resource constraints).
- Instead, we define a **tiny illustrative graph** over fertility concepts
  (AMH, ovarian reserve, age, PCOS, lifestyle changes).

Files:

- `graph_nodes.json` – list of medical/clinical concept nodes
- `graph_edges.json` – relationships between these nodes

`rag/rag.py` currently uses a simple keyword-based stub instead of a real
graph engine, but the folder structure is already compatible with a future
GraphRAG integration.
