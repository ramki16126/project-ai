# AI-POWERED RESUME RANKER - MINI PROJECT REPORT

## 1. Title
AI-Powered Resume Ranker Using NLP

## 2. Objective
The objective of this project is to automatically rank job candidates by comparing their resumes with a given job description using Natural Language Processing.

## 3. Problem Statement
Recruiters may need to review a large number of resumes for a single job. Manual screening can be time-consuming. This project provides an automated first-level screening system that ranks resumes according to their textual similarity to the job description.

## 4. Technologies Used
Python, Flask, spaCy, Scikit-learn, TF-IDF, cosine similarity, pypdf, HTML and CSS.

## 5. Methodology
### Step 1: Input
The user enters a job description and uploads multiple PDF resumes.

### Step 2: Text Extraction
The pypdf library extracts text from each resume.

### Step 3: Preprocessing
Text is converted to lowercase and processed with spaCy. Stop words, punctuation and very short tokens are removed.

### Step 4: Feature Extraction
TF-IDF converts text into numerical vectors. Unigrams and bigrams are used.

### Step 5: Similarity Calculation
Cosine similarity is calculated between the job description vector and each resume vector.

### Step 6: Ranking
Resumes are sorted by their similarity score in descending order.

### Step 7: Web Interface
Flask provides the web application. The interface displays rank, score and matched keywords.

## 6. Expected Output
Example:

Rank 1 - candidate1.pdf - 91.25%
Rank 2 - candidate3.pdf - 78.40%
Rank 3 - candidate2.pdf - 64.15%

## 7. Advantages
- Saves manual screening time.
- Supports multiple resumes.
- Easy web interface.
- Uses common NLP and machine learning techniques.
- Can be extended with skill weighting and semantic embeddings.

## 8. Limitations
- It mainly measures textual similarity.
- A high score does not guarantee that a candidate is suitable.
- Scanned/image-only PDFs may not contain extractable text.
- Keyword-based matching can miss synonyms.

## 9. Future Scope
- Add semantic embeddings using sentence-transformers.
- Add experience and education scoring.
- Add downloadable ranking reports.
- Store candidate results in a database.
- Add OCR for scanned resumes.

## 10. Conclusion
The project demonstrates a practical NLP application for automated resume screening. It combines PDF text extraction, preprocessing, TF-IDF, cosine similarity and Flask to provide a simple candidate ranking system.
