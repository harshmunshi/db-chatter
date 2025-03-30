# DB Chatter

A simple interactive chatbot that interfaces with SQLite databases using OpenAI's GPT models. This tool allows natural language queries to be converted into SQL commands, making database interactions more intuitive and accessible.

## Features

- Natural language to SQL query conversion
- SQLite database integration
- Interactive chat interface
- Personal information database management
- OpenAI GPT-3.5 Turbo integration

## Setup

### Prerequisites

- Python 3.6+
- OpenAI API key

### Installation

1. Clone the repository:
```bash
git clone https://github.com/harshmunshi/db-chatter.git
cd db-chatter
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the root directory and add your OpenAI API key:
```bash
OPENAI_API_KEY=your_api_key_here
```

## Usage

1. Initialize the database:
```bash
python create_database.py
```

2. Run the chatbot:
```bash
python openai_example.py
```

3. Start asking questions in natural language, for example:
   - "What is John's email address?"
   - "Show me all users with gmail accounts"
   - "Find the surname of the person with email john.doe@example.com"

## Database Schema

The database (`personal_info.db`) contains a single table with the following structure:

```sql
CREATE TABLE personal_info (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    surname TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE
)
```
## Acknowledgments

- OpenAI for providing the GPT API
- SQLite for the database engine

