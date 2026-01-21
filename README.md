# Cognito-Spec

A multi-agent web application Where Four AI Agents Transform Requirements Engineering! 

## 📋 Overview

Cognito-Spec is an advanced multi-agent system that works like a full RE team, ensuring every requirement is captured, clarified, structured, and validated without the usual gaps or inconsistencies.leverages OpenAI's Agent SDK to create intelligent, collaborative AI agents. 

Built on Streamlit for a seamless web interface, this application demonstrates the power of orchestrating multiple AI agents working together to solve complex tasks while maintaining persistent data storage through Firebase.

## 📋 Agents description

🎯 Agent 1 - The Elicitor: Conducts conversational interviews with context-aware questioning, ensuring no stakeholder insight is missed
🔍 Agent 2 - The Analyzer: Performs real-time classification, detects conflicts, and runs completeness checks as requirements flow in
📋 Agent 3 - The Specifier: Generates professional requirement documents automatically, structured and ready to use
✅ Agent 4 - The Validator: Conducts thorough gap analysis and completeness verification before you ship

Live Demo: https://cognito-spec.streamlit.app/

## 🛠️ Tech Stack

### Frontend
- **Streamlit** - Interactive web application framework
- **Python 3.8+** - Core programming language

### Backend
- **OpenAI Agent SDK** - Multi-agent orchestration and management
- **OpenAI API** - GPT models for intelligent responses
- **Agent Architecture** - Modular agent design with specialized capabilities

### Database
- **Firebase** - Cloud-based backend services
  - Firestore - NoSQL database for data persistence
  - Firebase Authentication - User management
  - Firebase Storage - File and media storage


## 🤖 Multi-Agent Architecture

This application implements a sophisticated multi-agent system using OpenAI's Agent SDK:

- **Agent Controller** (`ai_controller.py`) - Orchestrates multiple agents and manages their interactions
- **OpenAI Adapter** (`openai_adapter.py`) - Interfaces with OpenAI's Agent SDK for agent creation and management
- **Firebase Manager** (`firebase_manager.py`) - Handles data persistence for agent states and conversations
- **Specialized Agents** - Multiple agents with distinct roles and capabilities working collaboratively

## 🏗️ Project Structure

```
Cognito-Spec/
├── Home.py               # Main Streamlit application entry point
├── ai_controller.py      # Multi-agent orchestration and control flow
├── firebase_manager.py   # Firebase integration and database operations
├── openai_adapter.py     # OpenAI Agent SDK integration
├── requirements.txt      # Python dependencies
├── logooo.png            # Application logo
└── pages/                # Additional Streamlit pages for different agent interfaces
```

## 🚀 Features

- **Multi-Agent Collaboration**: Multiple AI agents working together using OpenAI's Agent SDK
- **Agent Orchestration**: Intelligent coordination between specialized agents
- **Real-time Interactions**: Dynamic conversations with AI agents
- **Firebase Integration**: Persistent storage for agent states, conversations, and user data
- **Multi-Page Interface**: Organized navigation for different agent functionalities
- **Modular Architecture**: Separate modules for agent control, Firebase operations, and OpenAI integration
- **Scalable Design**: Easy to add new agents and extend functionality

## 📦 Installation

### Prerequisites

- Python 3.8 or higher
- Firebase account and project
- OpenAI API key with access to Agent SDK

### Setup Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/HuzaifaNawaid/Cognito-Spec.git
   cd Cognito-Spec
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   
   Create a `.env` file in the root directory:
   ```env
   # OpenAI Configuration
   OPENAI_API_KEY=your_openai_api_key
   OPENAI_AGENT_SDK_KEY=your_agent_sdk_key
   
   # Firebase Configuration
   FIREBASE_CREDENTIALS=path_to_firebase_credentials.json
   FIREBASE_DATABASE_URL=your_firebase_database_url
   ```

5. **Set up Firebase**
   - Create a Firebase project at [Firebase Console](https://console.firebase.google.com/)
   - Enable Firestore Database
   - Enable Authentication (if required)
   - Download service account credentials (JSON file)
   - Place the JSON file in a secure location and update the path in `.env`

## 🎯 Usage

Run the Streamlit application:

```bash
streamlit run Home.py
```

The application will open in your default web browser at `http://localhost:8501`

## 📁 Module Descriptions

### `Home.py`
Main entry point for the Streamlit application. Provides the primary user interface, navigation logic, and initializes the multi-agent system.

### `ai_controller.py`
Core orchestration module for the multi-agent system. Manages agent lifecycle, coordinates interactions between agents, handles task delegation, and maintains conversation context.

### `firebase_manager.py`
Handles all Firebase operations:
- Agent state persistence
- Conversation history storage
- User data management
- Real-time data synchronization

### `openai_adapter.py`
Abstraction layer for OpenAI's Agent SDK:
- Agent creation and configuration
- API call management
- Model selection and optimization
- Error handling and fallback mechanisms

## 🏛️ Agent Architecture

The application follows a modular multi-agent architecture:

```
User Interface (Streamlit)
        ↓
Agent Controller (Orchestrator)
        ↓
Multiple Specialized Agents
        ↓
OpenAI Agent SDK
        ↓
Firebase (State Management)
```

Each agent can have:
- Specific domain expertise
- Unique prompt engineering
- Dedicated tools and capabilities
- Persistent memory through Firebase

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## 👤 Author

**Huzaifa Nawaid**
- GitHub: [@HuzaifaNawaid](https://github.com/HuzaifaNawaid)

## 🐛 Issues

Found a bug or have a suggestion? Please open an issue on the [GitHub Issues](https://github.com/HuzaifaNawaid/Cognito-Spec/issues) page.

## 📞 Support

For support and questions:
- Create an issue in the repository
- Check existing documentation
- Review the code comments and docstrings

## 🙏 Acknowledgments

- [Streamlit](https://streamlit.io/) - For the powerful web framework
- [OpenAI](https://openai.com/) - For Agent SDK and AI capabilities
- [Firebase](https://firebase.google.com/) - For reliable backend services
- The open-source community for continuous inspiration

## 📚 Resources

- [OpenAI Agent SDK Documentation](https://openai.github.io/openai-agents-python/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Firebase Documentation](https://firebase.google.com/docs)

---

**Built with multi-agent intelligence** 🤖 **by Huzaifa Nawaid** ❤️