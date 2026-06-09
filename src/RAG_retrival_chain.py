import os
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate

def get_qa_chain(vectordb, llm):
    # 1. Setup the retriever matching your logic
    retriever = vectordb.as_retriever(
        search_type="similarity_score_threshold",
        search_kwargs={"score_threshold": 0.7}
    )
    
    # 2. Keep your identical custom instructions intact
    prompt_template = """You are an assistant. Answer the question **only using the information provided in the context below**.  
Do not use any outside knowledge.  

Context: 
{context}

Question: 
{question}

Instructions:  
- If the answer can be found in the context, provide it concisely.  
- If the answer is not present in the context, reply exactly: "I don't know."
"""   

    PROMPT = PromptTemplate(
        template=prompt_template,
        input_variables=["context", "question"]
    )
    
    # 3. We create a clean custom runner object to mimic the old chain behavior perfectly
    class ModernRAGRunner:
        def __init__(self, retriever, llm, prompt):
            self.retriever = retriever
            self.llm = llm
            self.prompt = prompt
            
        def invoke(self, inputs):
            query = inputs.get("input") or inputs.get("query")
            # Pull matching source documents from your FAISS vector db
            docs = self.retriever.invoke(query)
            context_text = "\n\n".join([doc.page_content for doc in docs])
            
            # Format your prompt string cleanly
            formatted_prompt = self.prompt.format(context=context_text, question=query)
            
            # Send it off to Groq Llama 3
            response = self.llm.invoke(formatted_prompt)
            
            return {
                "answer": response.content,
                "context": docs
            }
            
    return ModernRAGRunner(retriever, llm, PROMPT)