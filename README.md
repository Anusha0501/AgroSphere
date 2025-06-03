
# 🌾 AgroSphere

Agrosphere is an AI-powered conversational assistant designed to support agricultural knowledge dissemination. It leverages modern language models, embedding techniques, and a local vector database to answer user queries based on agricultural documents.

## 🚀 Features

- Conversational AI chatbot trained on agricultural documents
- Uses Google Generative AI and Groq APIs
- Embedding storage with Chroma vector database
- Streamlit-based UI for quick interaction
- Environment-friendly design with smooth background

## 📁 Project Structure

```markdown

agrosphere/
├── agribot.py                  # Main chatbot application
├── embedding.py                # Script to create document embeddings
├── background.jpg              # UI background image
├── .env                        # Environment variables (API keys etc.)
├── my\_chroma\_store/            # Chroma vector database
├── Agriculture/inr.pdf         # Sample input document
├── venv/                       # Python virtual environment

```

## 🧪 Requirements

Python 3.8 or later and the following Python libraries:

```

streamlit
python-dotenv
langchain
langchain-community
langchain-google-genai
langchain-groq

````

You can install these using:

```bash
pip install -r requirements.txt
````

> You can create `requirements.txt` with:
>
> ```
> streamlit
> python-dotenv
> langchain
> langchain-community
> langchain-google-genai
> langchain-groq
> ```

## 🛠️ Setup Instructions

1. **Clone the Repository**

   ```bash
   git clone https://github.com/your-username/agrosphere.git
   cd agrosphere
   ```

2. **Create and Activate Virtual Environment (optional)**

   ```bash
   python -m venv venv
   source venv/bin/activate        # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set Environment Variables**

   Create a `.env` file in the project directory with:

   ```
   GOOGLE_API_KEY=your_google_api_key
   GROQ_API_KEY=your_groq_api_key
   ```

5. **Run the Chatbot**

   ```bash
   streamlit run agribot.py
   ```

## 🧠 Adding New Knowledge

To embed new documents, update or add files in the `Agriculture` folder and re-run:

```bash
python embedding.py
```

This regenerates the vector database using Chroma.

Made with ❤️ for smart farming by Anusha Singh.
