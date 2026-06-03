mkdir -p app
mkdir -p agents
mkdir -p db
mkdir -p workers
mkdir -p graph


touch app/agents/immigration_agent.py
touch app/agents/Timesheets_agent.py
touch app/agents/Payroll_agent.py
touch app/agents/Assignment_agent.py
touch app/agents/Document_agent.py
touch app/agents/Analytics_agent.py
touch app/workers/tasks.py
touch app/main.py
touch app/config.py
touch app/graph/state.py
touch app/graph/graph.py

touch app/api/__init__.py

touch .env
touch requirements.txt


echo "EISP_chatbot structure created successfully!"

