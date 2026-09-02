from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
from pypdf import PdfReader
import os
import re
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 10 * 1024 * 1024

ALLOWED_EXTENSIONS = {"pdf"}

# Uses spaCy for tokenization. No large model download is required.
nlp = spacy.blank("en")

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

def extract_pdf_text(file_storage):
    reader = PdfReader(file_storage)
    text = []
    for page in reader.pages:
        text.append(page.extract_text() or "")
    return "\n".join(text)

def clean_text(text):
    text = text.lower()
    doc = nlp(text)
    tokens = [
        token.text for token in doc
        if token.is_alpha and not token.is_stop and len(token.text) > 2
    ]
    return " ".join(tokens)

def get_score(job_description, resume_text):
    documents = [clean_text(job_description), clean_text(resume_text)]
    vectorizer = TfidfVectorizer(ngram_range=(1, 2), max_features=5000)
    matrix = vectorizer.fit_transform(documents)
    similarity = cosine_similarity(matrix[0:1], matrix[1:2])[0][0]
    return round(float(similarity) * 100, 2)

def extract_keywords(job_description):
    words = re.findall(r"[a-zA-Z][a-zA-Z+#.-]{2,}", job_description.lower())
    common = {
        "the", "and", "for", "with", "from", "that", "this", "are",
        "you", "will", "have", "has", "job", "work", "years", "using",
        "required", "skills", "experience", "candidate"
    }
    seen = []
    for word in words:
        if word not in common and word not in seen:
            seen.append(word)
    return seen[:30]

def matched_skills(job_description, resume_text):
    resume_lower = resume_text.lower()
    keywords = extract_keywords(job_description)
    return [k for k in keywords if k in resume_lower][:12]

@app.route("/", methods=["GET", "POST"])
def index():
    results = []
    error = None
    job_description = ""

    if request.method == "POST":
        job_description = request.form.get("job_description", "").strip()
        resumes = request.files.getlist("resumes")

        if not job_description:
            error = "Please enter a job description."
        elif not resumes or all(not r.filename for r in resumes):
            error = "Please upload at least one PDF resume."
        else:
            for resume in resumes:
                if not resume.filename:
                    continue
                if not allowed_file(resume.filename):
                    continue
                try:
                    text = extract_pdf_text(resume)
                    if not text.strip():
                        continue

                    score = get_score(job_description, text)
                    skills = matched_skills(job_description, text)

                    results.append({
                        "filename": secure_filename(resume.filename),
                        "score": score,
                        "skills": skills,
                    })
                except Exception as exc:
                    error = f"Could not process {resume.filename}: {exc}"

            results.sort(key=lambda x: x["score"], reverse=True)
            for i, result in enumerate(results, start=1):
                result["rank"] = i

            if not results and not error:
                error = "No readable PDF resumes were found."

    return render_template(
        "index.html",
        results=results,
        error=error,
        job_description=job_description
    )

if __name__ == "__main__":
    app.run(debug=True)
