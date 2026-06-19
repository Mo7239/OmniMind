from agents.orchestrator import Orchestrator

orch = Orchestrator()
orch.add_documents('data/docs/test.txt')

print('--- Researcher ---')
print(orch.route('what is OmniMind?'))

print('--- Summarizer ---')
print(orch.route('summarize the conversation'))