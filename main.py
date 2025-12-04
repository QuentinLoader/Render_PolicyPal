
from fastapi import FastAPI, Body
import openai
import firebase_admin
from firebase_admin import credentials, firestore
from docxtpl import DocxTemplate
import pdfkit
import os
import tempfile

# Initialize FastAPI
app = FastAPI()

# Initialize Firebase
cred = credentials.Certificate("64057e351b1c1f5ba74b2bbe35636268")
firebase_admin.initialize_app(cred)
db = firestore.client()

# Set OpenAI API Key
openai.api_key = os.getenv("9dea955c3ebb9aa71040ca135a4b732e")

@app.get("/")
def home():
    return {"message": "PolicyPal API is running"}

# ✅ AI Q&A Endpoint
@app.post("/ask")
def ask_compliance(question: str = Body(...)):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": question}]
        )
        answer = response.choices[0].message.content

        # Log to Firebase
        db.collection("logs").add({"query": question, "response": answer})

        return {"answer": answer}
    except Exception as e:
        return {"error": str(e)}

# ✅ Document Generation Endpoint
@app.post("/generate-document")
def generate_document(template_name: str = Body(...), context: dict = Body(...)):
    try:
        template_path = f"templates/{template_name}.docx"
        if not os.path.exists(template_path):
            return {"error": "Template not found"}

        # Load template and render
        doc = DocxTemplate(template_path)
        doc.render(context)

        # Save as DOCX
        temp_docx = tempfile.NamedTemporaryFile(delete=False, suffix=".docx")
        doc.save(temp_docx.name)

        # Convert to PDF
        temp_pdf = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
        pdfkit.from_file(temp_docx.name, temp_pdf.name)

        # Upload link simulation (in real case, upload to Firebase Storage)
        return {
            "message": "Document generated successfully",
            "docx_path": temp_docx.name,
            "pdf_path": temp_pdf.name
        }
    except Exception as e:
        return {"error": str(e)}
