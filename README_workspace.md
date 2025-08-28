# TITANS Workspace Integration

This document outlines the integration of the **TITANS** cognitive architecture with a web‑based workspace.  The goal of the TITANS workspace is to expose the agent’s capabilities—perception, episodic memory, semantic reasoning and planning—via a unified web interface.  It also enables collaborative interaction with external large language models through the OpenRouter proxy.

* **Architecture** – see `architecture_diagram.tex` for a high‑level diagram of the workspace, illustrating the core components: the web user interface, REST API, TITANS agent, episodic and semantic memory modules, and connectors to external models (GPT‑4, Claude, LM Studio etc.).
* **API** – the workspace provides a REST API for sending chat prompts, querying the knowledge graph and accessing memory.  Details are provided in `api_specification.md`.
* **Agents** – multiple agents can participate in the same workspace.  External LLMs are proxied via OpenRouter, while the TITANS agent is served locally and communicates via the REST interface defined in `TITANS_agent_interface.tex`.

This folder should be kept in sync with changes to the agent architecture (Milestones 2–5).