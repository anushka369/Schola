# Schola — School Homework Helper

# %%
import random
import math
import json
import ast
from dataclasses import dataclass, field
from typing import List, Dict, Any

# %%
def call_llm(prompt: str) -> str:
    if "explain" in prompt.lower():
        return "Step 1: Identify knowns. Step 2: Apply relevant formula. Step 3: Compute and simplify."
    if "hint" in prompt.lower():
        return "Try breaking the problem into smaller parts and solving each part first."
    return "I think the answer is: {}".format(random.choice(["42", "not sure", "check steps"]))

# %%
@dataclass
class Problem:
    id: str
    subject: str
    concept: str
    difficulty: int
    prompt: str
    solution: Any
    hints: List[str] = field(default_factory=list)

problem_bank: List[Problem] = [
    Problem("m1","math","addition",1,"What is 7 + 5?",12,["Add the digits"]),
    Problem("m2","math","multiplication",2,"What is 6 * 7?",42,["Multiply 6 by 7"]),
    Problem("m3","math","algebra",3,"Solve for x: 2*x + 3 = 11",4,["Isolate x"]),
    Problem("l1","lang","comprehension",2,"Read: 'The cat sat.' Q: Who sat?", "the cat",["Look for the subject"]),
    Problem("s1","science","gravity",2,"What pulls objects toward Earth?","gravity",["Think of falling objects"]) 
]

# %%
class ProgressManager:
    def __init__(self):
        self.students = {}
    def create_student(self, sid: str, profile: Dict = None):
        if profile is None:
            profile = {"mastery":{},"sessions":[]}
        self.students[sid] = profile
    def get_mastery(self, sid: str, concept: str):
        return self.students.get(sid, {}).get("mastery", {}).get(concept, 0.2)
    def update_mastery(self, sid: str, concept: str, delta: float):
        m = self.students.setdefault(sid, {}).setdefault("mastery", {}).get(concept, 0.0)
        nm = max(0.0, min(1.0, m + delta))
        self.students[sid]["mastery"][concept] = nm
    def log_session(self, sid: str, record: Dict):
        self.students.setdefault(sid, {}).setdefault("sessions", []).append(record)

# %%
class MathAgent:
    def generate_problem(self, concept: str, difficulty: int) -> Problem:
        candidates = [p for p in problem_bank if p.subject=="math" and p.concept==concept]
        if candidates:
            return random.choice(candidates)
        return random.choice([p for p in problem_bank if p.subject=="math"])
    def check_answer(self, problem: Problem, answer: str) -> Dict:
        try:
            if isinstance(problem.solution, (int,float)):
                tree = ast.parse(answer, mode='eval')
                val = eval(compile(tree, '<string>', 'eval'))
                correct = abs(float(val) - float(problem.solution)) < 1e-6
            else:
                correct = str(answer).strip().lower() == str(problem.solution).strip().lower()
        except Exception:
            correct = False
        feedback = call_llm(f"Explain: {problem.prompt}")
        return {"correct": correct, "feedback": feedback}

# %%
class LangAgent:
    def generate_problem(self, concept: str, difficulty: int) -> Problem:
        candidates = [p for p in problem_bank if p.subject=="lang"]
        return random.choice(candidates) if candidates else random.choice(problem_bank)
    def check_answer(self, problem: Problem, answer: str) -> Dict:
        correct = str(answer).strip().lower() == str(problem.solution).strip().lower()
        feedback = call_llm(f"Give hint: {problem.prompt}")
        return {"correct": correct, "feedback": feedback}

# %%
class AssessmentAgent:
    def __init__(self, pm: ProgressManager):
        self.pm = pm
    def select_next(self, sid: str, subject: str) -> Problem:
        concepts = list({p.concept for p in problem_bank if p.subject==subject})
        if not concepts:
            return random.choice(problem_bank)
        concept = random.choice(concepts)
        mastery = self.pm.get_mastery(sid, concept)
        target_difficulty = max(1, min(5, int(1 + mastery * 4)))
        candidates = [p for p in problem_bank if p.subject==subject and p.concept==concept]
        if not candidates:
            return random.choice(problem_bank)
        return random.choice(candidates)
    def update_after(self, sid: str, problem: Problem, correct: bool):
        delta = 0.1 if correct else -0.05
        self.pm.update_mastery(sid, problem.concept, delta)

# %%
class Orchestrator:
    def __init__(self):
        self.pm = ProgressManager()
        self.math_agent = MathAgent()
        self.lang_agent = LangAgent()
        self.assess = AssessmentAgent(self.pm)
    def start_session(self, sid: str):
        self.pm.create_student(sid)
    def ask_question(self, sid: str, subject: str):
        problem = self.assess.select_next(sid, subject)
        return problem
    def submit_answer(self, sid: str, problem: Problem, answer: str) -> Dict:
        if problem.subject == 'math':
            res = self.math_agent.check_answer(problem, answer)
        else:
            res = self.lang_agent.check_answer(problem, answer)
        self.assess.update_after(sid, problem, res["correct"])
        self.pm.log_session(sid, {"problem_id": problem.id, "correct": res["correct"]})
        return res

# Interactive session

# %%
orch = Orchestrator()
orch.start_session('student_1')
print('Welcome to Schola.')
for i in range(4):
    subj = random.choice(['math','lang'])
    prob = orch.ask_question('student_1', subj)
    print('\nProblem:', prob.prompt)
    ans = input('Your answer: ')
    out = orch.submit_answer('student_1', prob, ans)
    print('Correct:', out['correct'])
    print('Feedback:', out['feedback'])

# Simulated experiment (pre/post diagnostic)

# %%
def run_simulated_experiment(n_students=10):
    orch = Orchestrator()
    results = []
    for s in range(n_students):
        sid = f'sim_{s}'
        orch.start_session(sid)
        pre = 0
        for _ in range(5):
            p = orch.ask_question(sid, 'math')
            ans = str(p.solution) if random.random() < 0.5 else '0'
            r = orch.submit_answer(sid, p, ans)
            pre += int(r['correct'])
        for _ in range(10):
            p = orch.ask_question(sid, random.choice(['math','lang']))
            ans = str(p.solution) if random.random() < 0.6 else 'wrong'
            orch.submit_answer(sid, p, ans)
        post = 0
        for _ in range(5):
            p = orch.ask_question(sid, 'math')
            ans = str(p.solution) if random.random() < 0.7 else '0'
            r = orch.submit_answer(sid, p, ans)
            post += int(r['correct'])
        results.append({'sid': sid, 'pre': pre, 'post': post})
    return results

res = run_simulated_experiment(20)
print('Sample results (first 5):', res[:5])
