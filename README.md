# 🧠 Distributed NLP with Azure Durable Functions

This project demonstrates a serverless natural language processing pipeline using Azure Functions and Durable Orchestration. It was created for a Distributed Computing course to process large-scale text files by classifying verbs, generating statistics, and visualizing the output — all in a parallel, fault-tolerant, cloud-native environment.

## ⚙️ Project Overview

- **Function App (`function_app.py`)**: Extracts verbs and computes basic stats from text input.
- **Durable Orchestrator (`working_orchestrator.py`)**: Coordinates parallel invocation of functions across large file chunks.
- **JSON Configs**: Configure Azure Function runtime and local development (`host.json`, `local.settings.json`).
- **Visual Output**: Verb frequency histograms, pie charts, and summary statistics are generated for reporting.

## 📂 File Structure

| File                          | Description                                 |
|------------------------------|---------------------------------------------|
| `function_app.py`            | Azure Function that processes text chunks   |
| `working_orchestrator.py`    | Durable orchestrator to manage tasks        |
| `requirements.txt`           | Python dependencies                         |
| `local.settings.json`        | Local Azure Functions config                |
| `progress.json`              | Tracks orchestration progress               |
| `verb_histogram.png`         | Bar chart of most frequent verbs            |
| `verb_pie_chart.png`         | Pie chart of verb types                     |
| `verb_stats.png`             | Text summary of verb statistics             |

## 🔍 Features

- 🌩️ **Serverless Processing**: Run on Azure Functions with auto-scaling.
- ⚙️ **Orchestrated Execution**: Split and assign tasks using Azure Durable Functions.
- 🧠 **Natural Language Processing**: Verb extraction using Python NLP libraries (e.g., NLTK or spaCy).
- 📊 **Data Visualization**: Automatically generate charts and stats from processed text.
- 📦 **Modular JSON Configs**: Easy to configure locally or deploy to Azure.
