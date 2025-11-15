# Schola — School Homework Helper

A privacy-first, multi-agent tutoring agent that provides personalised, adaptive practice, and feedback for students with low-resource and limited access to live tutors. The system creates personalized practice, adapts question difficulty, and tracks student progress between sessions.

--- 

## Features
- Multi-agent orchestration (Orchestrator + Subject Specialists + Assessment agent)
- Session & long-term memory for student profiles
- Adaptive quizzes and immediate feedback
- Code execution sandbox for math answer checks
- Observability: logs and simple metrics

--- 

## Demo
1. Open `notebooks/demo.ipynb` in Jupyter notebook and run the cells top-to-bottom.
2. Follow the interactive cells to create a student profile and run a diagnostic.
3. Try a short practice session and view the progress summary.

---

## Project structure
```
├─ notebooks/
│  └─ demo.ipynb        # Kaggle demo notebook (main entrypoint)
├─ src/
│  ├─ orchestrator.py   # orchestration logic
│  ├─ agents/
│  │  ├─ math_agent.py
│  │  ├─ lang_agent.py
│  │  ├─ science_agent.py
│  │  └─ assessment_agent.py
│  ├─ memory.py         # progress manager / embeddings store
│  └─ tools.py          # code execution, search wrappers, utilities
├─ data/
│  ├─ problem_bank.csv
│  └─ sample_students.json
├─ tests/
│  ├─ test_agents.py
│  └─ test_safe_responses.py
├─ requirements.txt
└─ README.md

```
---

## Components
- **Multi-agent system:** Orchestrator routes to subject specialist agents and assessment agents.
- **Sessions & Memory:** Progress Manager stores student mastery and session summaries.
- **Tools:** Code execution verifies math solutions; optional search used for resource lookup.
- **Context engineering:** Session logs are compacted into short summaries for retrieval.
- **Observability:** Logs / traces stored in `logs/`; notebook generates plots.

---

## Safety & Privacy
- Use pseudonymous student IDs in sample data.
- No PII stored in the demo.
- Content filters to detect harmful instructions.

---

## Reproducing locally
1. Clone repo
2. `python -m venv venv && source venv/bin/activate`
3. `pip install -r requirements.txt`
4. Run `python -m src.server` (if using local demo)

---

## How to extend
- Add new subject specialist agents
- Replace the memory backend with a persistent DB
- Add human-in-the-loop mode for teacher reviews

---
