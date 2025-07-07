AI-powered MongoDB Query Generator API
This project is a simple backend built with FastAPI, MongoDB, and OpenAI, which receives natural language questions and returns filtered data from a MongoDB database by generating the appropriate queries through an LLM (Large Language Model).

It uses Docker to spin up a MongoDB instance pre-populated with example data (professors, classes, and scheduling), and a Python API that orchestrates the LLM prompt, executes the MongoDB query, and returns both the data and a concise human-readable answer.

🚀 Features
🔍 Accepts natural language questions via POST /chat endpoint.

🤖 Uses OpenAI GPT to generate JSON queries (find or aggregate) for MongoDB.

🗄️ Executes these queries on a MongoDB database.

📝 Returns both raw data and a short direct answer to the user's question.

🐳 Runs MongoDB with seeded data using Docker and an init script.

📂 Project Structure
graphql
Copiar
Editar
.
├── docker-compose.yml         # Docker service to run MongoDB with initial data
├── mongo-init.js              # Seeds the database with professors, classes, schedules
├── requirements.txt           # Python dependencies
├── main.py                    # FastAPI application
⚙️ Getting Started
1. Clone this repository
bash
Copiar
Editar
git clone https://your-repo-url.git
cd your-repo-folder
2. Start MongoDB with seeded data
bash
Copiar
Editar
docker-compose up -d
This will start MongoDB on localhost:27018 and seed it with:

professor collection

aula collection

agenda_professor collection

3. Install Python dependencies
Make sure you have Python 3.9+ installed.

bash
Copiar
Editar
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
4. Set your OpenAI API key
bash
Copiar
Editar
export OPENAI_API_KEY=your_key_here   # Linux/macOS
set OPENAI_API_KEY=your_key_here      # Windows CMD
$env:OPENAI_API_KEY="your_key_here"   # Windows PowerShell
🚀 Run the API
bash
Copiar
Editar
uvicorn main:app --reload
Your API will be available at:

cpp
Copiar
Editar
http://127.0.0.1:8000
🔥 Usage Example
Send a POST request to /chat with a JSON body:

json
Copiar
Editar
{
  "pergunta": "Which professor teaches Mathematics?"
}
The API will:

Use OpenAI to generate a MongoDB query.

Run this query on the seeded database.

Return:

the generated query,

the raw data from MongoDB,

and a short direct answer.

Sample response:

json
Copiar
Editar
{
  "query_gerada": "{ \"collection\": \"professor\", \"query\": { \"especialidade\": \"Matemática\" } }",
  "dados": [ { "_id": 1, "nome": "João Silva", "especialidade": "Matemática", ... } ],
  "resposta": "The professor who teaches Mathematics is João Silva."
}
🛠 Tech Stack
Python: FastAPI, Pydantic, PyMongo, OpenAI SDK

MongoDB: with seeded collections and indices

Docker Compose: for isolated database setup

📝 Notes
The MongoDB container exposes port 27018 on your local machine. Adjust if needed in docker-compose.yml.

The mongo-init.js script ensures consistent test data on startup.

The system is designed to avoid general $in with complex pipelines and always use $lookup for joins.

🚀 Future Improvements
Add authentication for API.

Include unit tests and pytest coverage.

Make LLM model configurable via ENV.

Containerize the FastAPI app for easier deployment.

📄 License
This project is released under the MIT License.