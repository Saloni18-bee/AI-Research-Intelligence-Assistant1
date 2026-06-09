from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from flask import Flask, render_template, request, jsonify

from src.load_and_extract_text import extract_text_from_pdf, extract_pdf_sections
from src.detect_and_split_sections import refine_sections, split_sections_with_content
from src.get_summary import generate_detailed_summary
from src.create_vector_db import create_vector_db
from src.RAG_retrival_chain import get_qa_chain


from dotenv import load_dotenv
import os, json

load_dotenv()

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

groq_api_key = os.getenv("GROQ_API_KEY")
llm_model = os.getenv("LLM_MODEL")
embedding_model = os.getenv("EMBEDDING_MODEL")

# Global variable
full_text = ''
Research_paper_topics = None
vector_db = None


llm  = ChatGroq(groq_api_key = groq_api_key, model_name = llm_model)

# Initialize embeddings using the Hugging Face model
embedder = HuggingFaceEmbeddings(model_name=embedding_model)

# print(llm.invoke("why diwali celebrate ?").content)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_pdf():
    global full_text
    global Research_paper_topics
    
    file = request.files.get('file')
    
    if not file:
        return jsonify({"error": "No file uploaded"}), 400
    
    filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    # print(filename)
    file.save(filename)
    
    # Get all topics name from research paper
    extracted_text = extract_text_from_pdf(filename)
    full_text = extracted_text
    extracted_sections = extract_pdf_sections(full_text=extracted_text)
    # print(extracted_sections)
    refined_sections = refine_sections(extracted_sections, llm)
    # print(refined_sections)
    section_with_content = split_sections_with_content(extracted_text, refined_sections)
    
    Research_paper_topics = section_with_content
    
    return jsonify({"topics": list(Research_paper_topics.keys())})


@app.route('/summary', methods=['POST'])
def get_summary():
    global Research_paper_topics
    
    topic = request.json.get('topic')
    # print(topic)
    
    topic_content = Research_paper_topics.get(topic, "No summary available.")
    
    summary = generate_detailed_summary(topic_content, llm)
    
    return jsonify({"summary": summary})
    

@app.route('/chat', methods=['POST'])
def chat():
    global full_text
    global vector_db
    
    user_message = request.json.get('message')
    print(user_message)
    
    if not vector_db:
        vectordb = create_vector_db(text=full_text, embedder=embedder)
        vector_db = vectordb
        
    chain = get_qa_chain(vectordb=vector_db, llm=llm)
    
    ai_response = chain.invoke(user_message)['result']
    print(ai_response)
    
    return jsonify({"response": ai_response})
        
    
    
    

if __name__ == "__main__":
    app.run(debug=True)
    
    # extracted_text = extract_text_from_pdf("paper.pdf")
    # print(extracted_text)
    # extracted_sections = extract_pdf_sections(full_text = extracted_text)
    # # with open("extracted_sections.json", "w") as f:
    # #     json.dump(extracted_sections, f, indent=4)
    
    # refined_sections = refine_sections(extracted_sections, llm)
    # # with open("refined_sections.json", "w") as f:
    # #     json.dump(refined_sections, f, indent=4)
    
    # section_with_content = split_sections_with_content(extracted_text, refined_sections)
    # with open("section_with_content.json", "w") as f:
    #     json.dump(section_with_content, f, indent=4)
    
    
    

import os
import json
from flask import Flask, render_template, request, jsonify
from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings
from dotenv import load_dotenv

# Import functions from your custom local src folder structure
from src.load_and_extract_text import extract_text_from_pdf, extract_pdf_sections
from src.detect_and_split_sections import refine_sections, split_sections_with_content
from src.get_summary import generate_detailed_summary
from src.create_vector_db import create_vector_db
from src.RAG_retrival_chain import get_qa_chain

# Load environment variables from your root .env file
load_dotenv()

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'

# Ensure upload directory exists safely
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

groq_api_key = os.getenv("GROQ_API_KEY")
llm_model = os.getenv("LLM_MODEL")
embedding_model = os.getenv("EMBEDDING_MODEL")

# Global session states
full_text = ''
Research_paper_topics = None
vector_db = None

# Initialize your AI Engines cleanly 
# (Note: modern class parameter is 'model', but model_name is fully fallback supported)
llm = ChatGroq(groq_api_key=groq_api_key, model=llm_model)
embedder = HuggingFaceEmbeddings(model_name=embedding_model)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload', methods=['POST'])
def upload_pdf():
    global full_text
    global Research_paper_topics
    
    file = request.files.get('file')
    if not file:
        return jsonify({"error": "No file uploaded"}), 400
    
    filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filename)
    
    # Process PDF and map out structural section topics
    extracted_text = extract_text_from_pdf(filename)
    full_text = extracted_text
    
    extracted_sections = extract_pdf_sections(full_text=extracted_text)
    refined_sections = refine_sections(extracted_sections, llm)
    section_with_content = split_sections_with_content(extracted_text, refined_sections)
    
    Research_paper_topics = section_with_content
    return jsonify({"topics": list(Research_paper_topics.keys())})


@app.route('/summary', methods=['POST'])
def get_summary():
    global Research_paper_topics
    
    if not Research_paper_topics:
        return jsonify({"error": "Please upload a research paper first."}), 400
        
    topic = request.json.get('topic')
    topic_content = Research_paper_topics.get(topic, "No content found for this section.")
    
    summary = generate_detailed_summary(topic_content, llm)
    return jsonify({"summary": summary})
    

@app.route('/chat', methods=['POST'])
def chat():
    global full_text
    global vector_db
    
    user_message = request.json.get('message')
    if not user_message:
        return jsonify({"error": "Empty message string received"}), 400
        
    # Lazy load vector DB chunk indices on the very first question request
    if not vector_db:
        if not full_text:
            return jsonify({"error": "No document content processed to chat against."}), 400
        vector_db = create_vector_db(text=full_text, embedder=embedder)
        
    # Get your newly modified custom pipeline runner
    chain = get_qa_chain(vectordb=vector_db, llm=llm)
    
    # FIX: Pass an inputs dictionary and parse out the modern 'answer' key response smoothly
    response_payload = chain.invoke({"input": user_message})
    ai_response = response_payload['answer']
    
    return jsonify({"response": ai_response})


if __name__ == "__main__":
    # Start local application hosting on port 5000
    app.run(debug=True, port=5000)