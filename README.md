# TITANS Legal Docs and Research Overview

This repository collects the legal, patent and strategic documentation for the **TITANS** project. TITANS (Technology for Intelligent Transformative Agents and Novel Self Improvement) is a modular cognitive architecture designed to produce self improving agents that learn from experience and collaborate with humans through natural language interfaces.

## Contents

- **Research overview** – [`titans_report.pdf`](titans_report.pdf) provides a concise research style summary of the architecture, milestones, agent interface, security measures and roadmap.
- **LaTeX sources** – The `.tex` files were generated from the original DOCX reports. They cover individual sections such as analysis, implementation plans and the agent interface.
- **Workspace documentation** – [`README_workspace.md`](README_workspace.md) outlines how the TITANS agent integrates with a web based workspace and REST API.
- **API specification** – [`api_specification.md`](api_specification.md) defines the REST endpoints used by the workspace and agents.

## How to use

1. **Read the overview** – Download and read [`titans_report.pdf`](titans_report.pdf) for a high level summary of the project suitable for dissemination or submission to arXiv.
2. **Compile LaTeX** – To generate your own PDFs from the `.tex` sources, use a TeX distribution (`pdflatex`) or a Python toolchain. Some templates require additional packages such as `amsmath`, `hyperref` and `lmodern`.
3. **Update** – When new milestones are achieved (e.g. implementation of the natural language interface or security hardening), update this README and regenerate the report accordingly.

## About TITANS

TITANS aims to bridge deep learning and symbolic reasoning by dividing the architecture into five milestones: perception (CapsNet + cross‟modal attention), long‟term memory, generative replay via variational autoencoders, abstraction and reasoning using Transformers and graph attention networks, and an agentic core employing Bayesian reinforcement learning. The project also includes a natural language interface and a security layer addressing supply‟chain attacks and privacy risks.

For more information about the agent interface and workspace, refer to `TITANS_agent_interface.tex` and the other specification files in this repository.
