# NotionAgent

An AI-powered conversational agent that reads and retrieves information from user's Notion workspace. Chat with your Notion data through a modern web interface.

## Features

- **User Authentication**: JWT-based cookie authentication
- **Personalized API Key Management**: Per-user OpenAI/Notion API key configuration
- **Notion Search**: Notion page search through LangGraph agent
- **Chat History**: Unlimited chat history storage and retrieval

## Screenshots

<div align="center">
  <img width="600" alt="Login Page" src="https://github.com/user-attachments/assets/610db64a-1cff-4760-9b7b-75a13ba4a72b" />
  <p><em>Login Page</em></p>
  
  <img width="600" alt="Chat Interface" src="https://github.com/user-attachments/assets/f05a8fc6-4329-43b6-a1dc-ccf34afe5e4c" />
  <p><em>Chat Interface with Message History</em></p>
  
  <img width="400" alt="Settings Modal" src="https://github.com/user-attachments/assets/52bd3fe9-9abc-4866-bb3d-53da05e569ed" />
  <p><em>Settings Configuration</em></p>
</div>


## Tech Stack

- **Backend**: FastAPI 0.121.2
- **AI**: LangChain 0.3.27, LangGraph 0.6.10, OpenAI
- **Database**: SQLAlchemy 2.0.44 + SQLite
- **Auth**: JWT (python-jose), bcrypt

## Installation

```bash
# 1. Create and activate Python virtual environment
python -m venv .venv
source .venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure environment variables (Create .env file and set a strong secret key)
SECRET_KEY=your-jwt-secret-key

# 4. Run server
uvicorn backend.main:app --reload
```

## API Endpoints
📚 **API Docs(Swagger)**: [http://localhost:8000/docs](http://localhost:8000/docs)

### Authentication
- `POST /api/v1/auth/register` - User registration
- `POST /api/v1/auth/login` - User login
- `POST /api/v1/auth/logout` - User logout
- `GET /api/v1/auth/me` - Get current user info

### Settings
- `POST /api/v1/settings` - Configure API keys (OpenAI, Notion)
- `GET /api/v1/settings` - Get settings

### Chat
- `POST /api/v1/chat` - Send message
- `GET /api/v1/chat/history?thread_id={thread_id}` - Get chat history

## Project Structure

```
backend/          # FastAPI backend
  ├── api/
  │   └── v1/     # API v1 endpoints
  ├── core/       # Security, dependencies, settings
  ├── db/         # Database models & setup
  └── main.py     # FastAPI application
agent/            # LangGraph agent
  ├── clients/    # Notion API client
  ├── graph/      # Graph definition & nodes
  ├── tools/      # Notion tool integration
  ├── settings.py # Agent configuration
  └── main.py
requirements.txt      # Production dependencies
dev-requirements.txt  # Development dependencies
```

## Usage

1. Register and login
2. Configure OpenAI API key, Notion API key, and Notion page ID in settings
3. Search Notion information through chat

## Frontend

- Frontend Repository: [NotionAgentFront](https://github.com/seojoo21/NotionAgentFront)
