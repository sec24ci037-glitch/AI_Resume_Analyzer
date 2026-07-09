from flask import Flask, render_template, request
import os
import pdfplumber

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# List of skills to search for
skills_list = [
    "python", "java", "c", "c++", "html", "css", "javascript",
    "sql", "mysql", "flask", "django", "react", "node.js",
    "git", "github", "machine learning", "ai"
]

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():

    if "resume" not in request.files:
        return "No file uploaded"

    file = request.files["resume"]

    if file.filename == "":
        return "Please select a PDF"

    filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
    file.save(filepath)

    text = ""

    with pdfplumber.open(filepath) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text.lower()

    found_skills = []

    for skill in skills_list:
        if skill.lower() in text:
            found_skills.append(skill)

    ats_score = min(len(found_skills) * 10, 100)

    suggestions = []

    if "python" not in found_skills:
        suggestions.append("Add Python")

    if "sql" not in found_skills:
        suggestions.append("Add SQL")

    if "git" not in found_skills:
        suggestions.append("Add Git")

    if "flask" not in found_skills:
        suggestions.append("Add Flask")

    return render_template(
        "index.html",
        score=ats_score,
        skills=found_skills,
        suggestions=suggestions,
        text=text
    )


if __name__ == "__main__":
    app.run(debug=True)