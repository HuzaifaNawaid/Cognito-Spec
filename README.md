# Cognito-Spec

A Streamlit-based application that integrates AI capabilities with Firebase backend and OpenAI services.

## 📋 Overview

Cognito-Spec is a web application built with Streamlit that provides an AI-powered interface for users. The application leverages Firebase for data management and OpenAI for intelligent responses and interactions.

## 🏗️ Project Structure

```
Cognito-Spec/
├── Home.py                 # Main Streamlit application entry point
├── ai_controller.py        # AI logic and control flow
├── firebase_manager.py     # Firebase integration and database operations
├── openai_adapter.py       # OpenAI API integration
├── requirements.txt        # Python dependencies
├── logooo.png             # Application logo
└── pages/                 # Additional Streamlit pages
```

## 🚀 Features

- **AI-Powered Interface**: Intelligent interactions powered by OpenAI
- **Firebase Integration**: Secure data storage and retrieval
- **Multi-Page Application**: Organized navigation with Streamlit pages
- **Modular Architecture**: Separate modules for AI control, Firebase operations, and OpenAI integration

## 📦 Installation

### Prerequisites

- Python 3.8 or higher
- Firebase account and credentials
- OpenAI API key

### Setup Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/HuzaifaNawaid/Cognito-Spec.git
   cd Cognito-Spec
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables**
   
   Create a `.env` file in the root directory with the following:
   ```env
   OPENAI_API_KEY=your_openai_api_key
   FIREBASE_CREDENTIALS=path_to_firebase_credentials.json
   # Add other necessary environment variables
   ```

4. **Set up Firebase**
   - Download your Firebase service account credentials
   - Place the JSON file in a secure location
   - Update the path in your environment variables

## 🎯 Usage

Run the Streamlit application:

```bash
streamlit run Home.py
```

The application will open in your default web browser at `http://localhost:8501`

## 🔧 Configuration

### Firebase Setup

Ensure your Firebase project is configured with:
- Firestore database
- Authentication (if required)
- Storage buckets (if needed)

### OpenAI Integration

Configure your OpenAI API settings in the `openai_adapter.py` module or through environment variables.

## 📁 Module Descriptions

### `Home.py`
Main entry point for the Streamlit application. Contains the primary user interface and navigation logic.

### `ai_controller.py`
Manages AI logic, prompt engineering, and coordinates between the UI and AI services.

### `firebase_manager.py`
Handles all Firebase operations including:
- Database reads and writes
- Authentication management
- Data validation

### `openai_adapter.py`
Provides an abstraction layer for OpenAI API calls, making it easier to:
- Switch between different OpenAI models
- Handle API errors gracefully
- Implement retry logic

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

For support and questions, please create an issue in the repository.

## 🙏 Acknowledgments

- [Streamlit](https://streamlit.io/) - For the amazing web framework
- [OpenAI](https://openai.com/) - For AI capabilities
- [Firebase](https://firebase.google.com/) - For backend services

---

Made with ❤️ by Huzaifa Nawaid