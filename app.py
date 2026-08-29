from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_sqlalchemy import SQLAlchemy
import os
import PyPDF2

app = Flask(__name__)

UPLOAD_FOLDER = os.path.join(app.root_path, "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

app.secret_key = os.environ.get(
    "SECRET_KEY",
    "prepai-local-development-key"
)

# ----------------------------
# Database Configuration
# ----------------------------
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Create database object
db = SQLAlchemy(app)

# ----------------------------
# Student Table
# ----------------------------
class Student(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100), nullable=False)

    email = db.Column(db.String(100), unique=True, nullable=False)

    mobile = db.Column(db.String(15), nullable=False)

    college = db.Column(db.String(150), nullable=False)

    course = db.Column(db.String(50), nullable=False)

    graduation = db.Column(db.String(10), nullable=False)

    password = db.Column(db.String(200), nullable=False)


class AptitudeScore(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    student_email = db.Column(db.String(100), nullable=False)

    score = db.Column(db.Integer, nullable=False)

    total = db.Column(db.Integer, nullable=False)

class CodingScore(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    student_email = db.Column(db.String(100), nullable=False)

    score = db.Column(db.Integer, nullable=False)

    total = db.Column(db.Integer, nullable=False)

class InterviewScore(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    student_email = db.Column(db.String(100), nullable=False)

    score = db.Column(db.Integer, nullable=False)

    total = db.Column(db.Integer, nullable=False)

class ResumeScore(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    student_email = db.Column(
        db.String(100),
        nullable=False
    )

    score = db.Column(
        db.Integer,
        nullable=False
    )

    total = db.Column(
        db.Integer,
        nullable=False
    )


# ----------------------------
# Routes
# ----------------------------

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        student = Student.query.filter_by(
            email=email,
            password=password
        ).first()

        if student:

            session["student_name"] = student.name
            session["student_email"] = student.email

            return redirect(url_for("dashboard"))

        else:
            return "<h2>Invalid Email or Password!</h2>"

    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        mobile = request.form["mobile"]
        college = request.form["college"]
        course = request.form["course"]
        graduation = request.form["graduation"]
        password = request.form["password"]

        # Check if email already exists
        existing_student = Student.query.filter_by(email=email).first()

        if existing_student:
            return "<h2>Email already registered! Please use another email.</h2>"

        student = Student(
            name=name,
            email=email,
            mobile=mobile,
            college=college,
            course=course,
            graduation=graduation,
            password=password
        )

        db.session.add(student)
        db.session.commit()

        return redirect(url_for("login"))

    return render_template("register.html")


@app.route("/dashboard")
def dashboard():

    if "student_email" not in session:
        return redirect(url_for("login"))

    # Get latest aptitude score
    latest_score = AptitudeScore.query.filter_by(
        student_email=session["student_email"]
    ).order_by(AptitudeScore.id.desc()).first()

    if latest_score:
        aptitude_score = latest_score.score
        total_score = latest_score.total
        placement_percentage = int((aptitude_score / total_score) * 100)
    else:
        aptitude_score = 0
        total_score = 0
        placement_percentage = 0

    # Get latest coding score
    latest_coding = CodingScore.query.filter_by(
        student_email=session["student_email"]
    ).order_by(CodingScore.id.desc()).first()

    if latest_coding:
        coding_score = f"{latest_coding.score} / {latest_coding.total}"
    else:
        coding_score = "Coming Soon"

    print("Latest Coding:", latest_coding)

    if latest_coding:
        print("Coding Score:", latest_coding.score, "/", latest_coding.total)

    # Get latest interview score
    latest_interview = InterviewScore.query.filter_by(
        student_email=session["student_email"]
    ).order_by(InterviewScore.id.desc()).first()

    if latest_interview:
        interview_score = f"{latest_interview.score} / {latest_interview.total}"
    else:
        interview_score = "Not Attempted"

    return render_template(
        "dashboard.html",
        student_name=session["student_name"],
        student_email=session["student_email"],
        aptitude_score=aptitude_score,
        total_score=total_score,
        placement_percentage=placement_percentage,
        coding_score=coding_score,
        interview_score=interview_score
    )

@app.route("/aptitude")
def aptitude():

    if "student_name" not in session:
        return redirect(url_for("login"))

    return render_template(
        "aptitude.html",
        student_name=session["student_name"]
    )

@app.route("/coding")
def coding():

    if "student_email" not in session:
        return redirect(url_for("login"))

    return render_template("coding.html")

@app.route("/submit_coding", methods=["POST"])
def submit_coding():

    if "student_email" not in session:
        return redirect(url_for("login"))

    code = request.form["code"]

    # Temporary evaluation
    score = 8
    total = 10

    coding = CodingScore(
        student_email=session["student_email"],
        score=score,
        total=total
    )

    db.session.add(coding)
    db.session.commit()

    return redirect(url_for("dashboard"))

@app.route("/resume", methods=["GET", "POST"])
def resume():

    if "student_email" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":

        file = request.files.get("resume")

        if not file or file.filename == "":
            return render_template(
                "resume.html",
                error="Please select a resume PDF."
            )

        filepath = os.path.join(
            app.config["UPLOAD_FOLDER"],
            file.filename
        )

        file.save(filepath)

        text = ""

        try:

            with open(filepath, "rb") as pdf_file:

                reader = PyPDF2.PdfReader(pdf_file)

                for page in reader.pages:
                    text += page.extract_text() or ""

        except Exception:

            return render_template(
                "resume.html",
                error="Unable to read this PDF. Please upload a valid resume."
            )

        text = text.lower()


        # Skills checked by the analyzer

        skill_list = [
            "python",
            "java",
            "c++",
            "html",
            "css",
            "javascript",
            "flask",
            "sql",
            "machine learning",
            "deep learning",
            "artificial intelligence",
            "ai",
            "numpy",
            "pandas",
            "power bi",
            "excel",
            "git",
            "github"
        ]


        # Find skills

        skills = []

        for skill in skill_list:

            if skill in text:
                skills.append(skill)


        # Calculate resume score

        score = int(
            (len(skills) / len(skill_list)) * 100
        )

        if score > 100:
            score = 100


        # Save resume score to database

        resume_score = ResumeScore.query.filter_by(
            student_email=session["student_email"]
        ).first()

        if resume_score:

            resume_score.score = score
            resume_score.total = 100

        else:

            resume_score = ResumeScore(
                student_email=session["student_email"],
                score=score,
                total=100
            )

            db.session.add(resume_score)

        db.session.commit()


        # Determine resume strength

        if score >= 80:

            strength = "Excellent"

            message = (
                "Your resume contains a strong set of technical skills."
            )

        elif score >= 60:

            strength = "Good"

            message = (
                "Your resume is good, but you can add more relevant skills "
                "and projects."
            )

        elif score >= 40:

            strength = "Average"

            message = (
                "Your resume has some useful skills, but it needs improvement."
            )

        else:

            strength = "Needs Improvement"

            message = (
                "Your resume should include more technical skills, "
                "projects and relevant experience."
            )


        # Find missing skills

        missing_skills = [
            skill
            for skill in skill_list
            if skill not in skills
        ]


        # Suggestions

        suggestions = []


        if "python" not in skills:

            suggestions.append(
                "Add Python if you are targeting software or AI/ML roles."
            )


        if "sql" not in skills:

            suggestions.append(
                "Add SQL and database knowledge."
            )


        if "machine learning" not in skills:

            suggestions.append(
                "Consider adding Machine Learning for AI/ML positions."
            )


        if "github" not in skills:

            suggestions.append(
                "Add GitHub projects to demonstrate your practical work."
            )


        suggestions.append(
            "Include 2-3 strong academic or personal projects."
        )


        suggestions.append(
            "Keep your resume concise and easy to read."
        )


        # Show result

        return render_template(
            "resume_result.html",
            score=score,
            skills=skills,
            missing_skills=missing_skills,
            strength=strength,
            message=message,
            suggestions=suggestions
        )


    return render_template("resume.html")

@app.route("/save_score", methods=["POST"])
def save_score():

    if "student_email" not in session:
        return jsonify({"status": "error"})

    data = request.get_json()

    score = AptitudeScore(
        student_email=session["student_email"],
        score=data["score"],
        total=data["total"]
    )

    db.session.add(score)
    db.session.commit()

    return jsonify({"status": "success"})

@app.route("/mock_interview")
def mock_interview():

    if "student_email" not in session:
        return redirect(url_for("login"))

    return render_template("mock_interview.html")

@app.route("/interview_score", methods=["POST"])
def interview_score():

    if "student_email" not in session:
        return jsonify({
            "status": "error",
            "message": "Please login first."
        }), 401

    data = request.get_json()

    score = int(data.get("score", 0))

    # Make sure score stays between 0 and 100
    if score < 0:
        score = 0

    if score > 100:
        score = 100

    # Feedback
    if score >= 80:

        feedback = "Excellent communication skills."

    elif score >= 60:

        feedback = "Good performance. Keep practicing."

    else:

        feedback = "Needs improvement. Practice more interviews."


    # --------------------------------
    # SAVE INTERVIEW SCORE
    # --------------------------------

    existing_score = InterviewScore.query.filter_by(
        student_email=session["student_email"]
    ).first()


    if existing_score:

        existing_score.score = score
        existing_score.total = 100

    else:

        new_score = InterviewScore(
            student_email=session["student_email"],
            score=score,
            total=100
        )

        db.session.add(new_score)


    db.session.commit()


    return jsonify({
        "status": "success",
        "score": score,
        "feedback": feedback
    })

@app.route("/recommendation")
def recommendation():

    if "student_email" not in session:
        return redirect(url_for("login"))

    aptitude = AptitudeScore.query.filter_by(
        student_email=session["student_email"]
    ).order_by(AptitudeScore.id.desc()).first()

    coding = CodingScore.query.filter_by(
        student_email=session["student_email"]
    ).order_by(CodingScore.id.desc()).first()

    interview = InterviewScore.query.filter_by(
        student_email=session["student_email"]
    ).order_by(InterviewScore.id.desc()).first()

    aptitude_score = aptitude.score if aptitude else 0
    coding_score = coding.score if coding else 0
    interview_score = interview.score if interview else 0

    average = int(
        (aptitude_score + coding_score + interview_score) / 3
    )

    if average >= 85:

        companies = [
            "Google",
            "Microsoft",
            "Amazon",
            "Adobe",
            "Oracle"
        ]

    elif average >= 70:

        companies = [
            "Infosys",
            "TCS",
            "Wipro",
            "Accenture",
            "Capgemini"
        ]

    else:

        companies = [
            "Continue Practicing",
            "Improve Coding",
            "Improve Aptitude",
            "Practice Interviews"
        ]

    return render_template(
        "recommendation.html",
        companies=companies,
        average=average
    )

@app.route("/companies", methods=["GET", "POST"])
def companies():

    if "student_email" not in session:
        return redirect(url_for("login"))

    recommendations = {

        "TCS": {
            "skills": ["Python", "Java", "SQL", "Web Development"],
            "roles": ["Software Developer", "Web Developer", "Data Analyst"]
        },

        "Infosys": {
            "skills": ["Python", "Java", "SQL", "Web Development"],
            "roles": ["Software Developer", "System Engineer", "Data Analyst"]
        },

        "Wipro": {
            "skills": ["Python", "Java", "Web Development", "SQL"],
            "roles": ["Software Developer", "Web Developer", "Testing Engineer"]
        },

        "Accenture": {
            "skills": ["Python", "Java", "Web Development", "AI/ML", "SQL"],
            "roles": ["Software Developer", "AI Engineer", "Data Analyst"]
        },

        "Cognizant": {
            "skills": ["Python", "Java", "SQL", "Web Development"],
            "roles": ["Programmer Analyst", "Software Developer", "Data Analyst"]
        },

        "Google": {
            "skills": ["Python", "Java", "AI/ML", "SQL"],
            "roles": ["Software Engineer", "Machine Learning Engineer", "Data Scientist"]
        },

        "Microsoft": {
            "skills": ["Python", "Java", "AI/ML", "SQL"],
            "roles": ["Software Engineer", "AI Engineer", "Data Scientist"]
        },

        "Amazon": {
            "skills": ["Python", "Java", "AI/ML", "SQL", "Web Development"],
            "roles": ["Software Development Engineer", "Data Engineer", "AI Engineer"]
        },

        "IBM": {
            "skills": ["Python", "Java", "AI/ML", "SQL"],
            "roles": ["AI Engineer", "Data Scientist", "Software Developer"]
        },

        "Capgemini": {
            "skills": ["Java", "Python", "SQL", "Web Development"],
            "roles": ["Software Engineer", "Web Developer", "Data Analyst"]
        }
    }

    results = []

    if request.method == "POST":

        selected_skills = request.form.getlist("skills")

        for company, details in recommendations.items():

            matching_skills = [
                skill
                for skill in selected_skills
                if skill in details["skills"]
            ]

            if selected_skills:

                match_percentage = int(
                    (len(matching_skills) / len(selected_skills)) * 100
                )

            else:
                match_percentage = 0

            if match_percentage > 0:

                results.append({
                    "name": company,
                    "match": match_percentage,
                    "skills": matching_skills,
                    "roles": details["roles"]
                })

        results.sort(
            key=lambda x: x["match"],
            reverse=True
        )

    return render_template(
        "companies.html",
        companies=results
    )

@app.route("/profile")
def profile():

    if "student_email" not in session:
        return redirect(url_for("login"))

    student = Student.query.filter_by(
        email=session["student_email"]
    ).first()

    return render_template(
        "profile.html",
        student=student
    )

@app.route("/placement")
def placement():

    if "student_email" not in session:
        return redirect(url_for("login"))

    aptitude = 80
    coding = 75
    resume = 90
    interview = 85

    overall = int(
        (aptitude + coding + resume + interview)/4
    )

    if overall >= 80:

        message = "🟢 Excellent Placement Chances"

    elif overall >= 60:

        message = "🟡 Good Placement Chances"

    else:

        message = "🔴 Need More Practice"

    return render_template(

        "placement.html",

        aptitude=aptitude,

        coding=coding,

        resume=resume,

        interview=interview,

        overall=overall,

        message=message

    )

@app.route("/interview")
def interview():

    if "student_email" not in session:
        return redirect(url_for("login"))

    return render_template("interview.html")

@app.route("/submit_interview", methods=["POST"])
def submit_interview():

    if "student_email" not in session:
        return redirect(url_for("login"))

    print("CURRENT STUDENT EMAIL:", session["student_email"])
    print("CURRENT STUDENT NAME:", session.get("student_name"))

    email = session["student_email"]

    answer1 = request.form.get("answer1", "").strip()
    answer2 = request.form.get("answer2", "").strip()
    answer3 = request.form.get("answer3", "").strip()

    # Calculate score
    score = 0

    if len(answer1) > 30:
        score += 30

    if len(answer2) > 30:
        score += 35

    if len(answer3) > 30:
        score += 35

    # Find existing interview score for this student
    interview_score = InterviewScore.query.filter_by(
        student_email=email
    ).first()

    if interview_score:

        # Update existing score
        interview_score.score = score
        interview_score.total = 100

    else:

        # Create new score
        interview_score = InterviewScore(
            student_email=email,
            score=score,
            total=100
        )

        db.session.add(interview_score)

    db.session.commit()

    return render_template(
        "interview_result.html",
        score=score
    )

@app.route("/career", methods=["GET", "POST"])
def career():

    if "student_email" not in session:
        return redirect(url_for("login"))

    roadmap = []
    selected_career = ""

    career_roadmaps = {

        "Python Developer": [
            {
                "title": "Learn Python",
                "description": "Learn Python syntax, variables, functions, loops and data structures.",
                "duration": "2-3 Weeks"
            },
            {
                "title": "Learn Object-Oriented Programming",
                "description": "Understand classes, objects, inheritance and polymorphism.",
                "duration": "1-2 Weeks"
            },
            {
                "title": "Learn Flask",
                "description": "Build web applications and understand Flask routing and templates.",
                "duration": "2 Weeks"
            },
            {
                "title": "Learn SQL",
                "description": "Learn databases, queries, joins and CRUD operations.",
                "duration": "1-2 Weeks"
            },
            {
                "title": "Build Projects",
                "description": "Create real-world Python and Flask projects for your portfolio.",
                "duration": "2-4 Weeks"
            },
            {
                "title": "Prepare for Interviews",
                "description": "Practice Python coding questions and technical interview questions.",
                "duration": "1-2 Weeks"
            }
        ],


        "Full Stack Developer": [
            {
                "title": "HTML",
                "description": "Learn webpage structure, forms, tables and semantic HTML.",
                "duration": "1 Week"
            },
            {
                "title": "CSS",
                "description": "Learn layouts, Flexbox, Grid, responsive design and styling.",
                "duration": "1-2 Weeks"
            },
            {
                "title": "JavaScript",
                "description": "Learn variables, functions, DOM manipulation and events.",
                "duration": "2-3 Weeks"
            },
            {
                "title": "Backend Development",
                "description": "Learn Flask, APIs, routing and server-side programming.",
                "duration": "2-3 Weeks"
            },
            {
                "title": "SQL & Databases",
                "description": "Learn database design, queries and connecting applications to databases.",
                "duration": "1-2 Weeks"
            },
            {
                "title": "Build Full Stack Projects",
                "description": "Create complete web applications combining frontend and backend.",
                "duration": "3-4 Weeks"
            }
        ],


        "AI/ML Engineer": [
            {
                "title": "Learn Python",
                "description": "Build a strong Python programming foundation.",
                "duration": "2-3 Weeks"
            },
            {
                "title": "Learn NumPy & Pandas",
                "description": "Learn numerical computing and data manipulation.",
                "duration": "1-2 Weeks"
            },
            {
                "title": "Learn Statistics",
                "description": "Understand probability, statistics and concepts used in machine learning.",
                "duration": "2 Weeks"
            },
            {
                "title": "Machine Learning",
                "description": "Learn regression, classification, clustering and model evaluation.",
                "duration": "3-4 Weeks"
            },
            {
                "title": "Deep Learning",
                "description": "Learn neural networks and deep learning fundamentals.",
                "duration": "3-4 Weeks"
            },
            {
                "title": "Build AI Projects",
                "description": "Create machine learning and AI projects for your portfolio.",
                "duration": "3-4 Weeks"
            },
            {
                "title": "AI/ML Interview Preparation",
                "description": "Practice machine learning concepts, coding and technical interviews.",
                "duration": "2 Weeks"
            }
        ],


        "Data Analyst": [
            {
                "title": "Learn Excel",
                "description": "Learn formulas, pivot tables, charts and data cleaning.",
                "duration": "1-2 Weeks"
            },
            {
                "title": "Learn SQL",
                "description": "Learn queries, joins, grouping and database analysis.",
                "duration": "1-2 Weeks"
            },
            {
                "title": "Learn Python",
                "description": "Learn Python for data analysis and automation.",
                "duration": "2 Weeks"
            },
            {
                "title": "Learn Pandas",
                "description": "Analyze and manipulate datasets using Pandas.",
                "duration": "1-2 Weeks"
            },
            {
                "title": "Data Visualization",
                "description": "Create charts and dashboards using visualization tools.",
                "duration": "1-2 Weeks"
            },
            {
                "title": "Power BI",
                "description": "Build interactive dashboards and business reports.",
                "duration": "2 Weeks"
            },
            {
                "title": "Build Data Projects",
                "description": "Create real-world data analysis projects for your portfolio.",
                "duration": "2-3 Weeks"
            }
        ]
    }


    if request.method == "POST":

        selected_career = request.form.get("career")

        roadmap = career_roadmaps.get(
            selected_career,
            []
        )


    return render_template(
        "career.html",
        roadmap=roadmap,
        selected_career=selected_career
    )


@app.route("/chatbot", methods=["GET", "POST"])
def chatbot():

    if "student_email" not in session:
        return redirect(url_for("login"))

    user_message = ""
    bot_response = ""

    if request.method == "POST":

        user_message = request.form.get("message", "").strip()

        message = user_message.lower()


        if "python" in message:

            bot_response = (
                "Python is an excellent skill for placements. "
                "Start with variables, conditions, loops, functions, "
                "data structures, OOP and then move to projects."
            )


        elif "interview" in message:

            bot_response = (
                "For interviews, prepare in four areas: "
                "aptitude, technical concepts, coding and HR questions. "
                "Also practice explaining your projects clearly."
            )


        elif "aptitude" in message:

            bot_response = (
                "For aptitude preparation, focus on percentages, "
                "profit and loss, ratios, averages, time and work, "
                "number systems and logical reasoning."
            )


        elif "resume" in message:

            bot_response = (
                "A good fresher resume should highlight your education, "
                "technical skills, projects, certifications and achievements. "
                "Keep it clear and preferably one page."
            )


        elif "career" in message or "job" in message:

            bot_response = (
                "Choose a career based on your interests and strengths. "
                "For software roles, build programming skills and projects. "
                "For AI/ML roles, focus on Python, mathematics, data analysis "
                "and machine learning."
            )


        elif "java" in message:

            bot_response = (
                "For Java interviews, focus on OOP concepts, classes, "
                "objects, inheritance, polymorphism, exception handling, "
                "collections and basic coding problems."
            )


        elif "sql" in message or "database" in message:

            bot_response = (
                "For SQL interviews, practice SELECT queries, WHERE, "
                "GROUP BY, ORDER BY, JOINs, subqueries and aggregate functions."
            )


        elif "project" in message:

            bot_response = (
                "For placements, try to build 2-3 meaningful projects. "
                "Be ready to explain the problem, technologies used, "
                "your contribution and the results."
            )


        elif "hello" in message or "hi" in message:

            bot_response = (
                "Hello! 👋 I'm your PrepAI placement assistant. "
                "You can ask me about interviews, aptitude, coding, "
                "Python, Java, SQL, resumes or careers."
            )


        else:

            bot_response = (
                "I'm your placement preparation assistant. "
                "Try asking me about Python, Java, SQL, aptitude, "
                "interviews, resumes, projects or career guidance."
            )


    return render_template(
        "chatbot.html",
        user_message=user_message,
        bot_response=bot_response
    )

@app.route("/admin")
def admin():

    students = Student.query.all()

    total_students = Student.query.count()
    total_aptitude = AptitudeScore.query.count()
    total_coding = CodingScore.query.count()
    total_interviews = InterviewScore.query.count()

    return render_template(
        "admin.html",
        students=students,
        total_students=total_students,
        total_aptitude=total_aptitude,
        total_coding=total_coding,
        total_interviews=total_interviews
    )


@app.route("/progress")
def progress():

    if "student_email" not in session:
        return redirect(url_for("login"))

    email = session["student_email"]

    # -----------------------------
    # APTITUDE
    # -----------------------------

    aptitude = AptitudeScore.query.filter_by(
        student_email=email
    ).order_by(
        AptitudeScore.id.desc()
    ).first()

    aptitude_score = aptitude.score if aptitude else 0
    aptitude_total = aptitude.total if aptitude else 0

    if aptitude and aptitude.total > 0:
        aptitude_percent = round(
            (aptitude.score / aptitude.total) * 100
        )
    else:
        aptitude_percent = 0


    # -----------------------------
    # CODING
    # -----------------------------

    coding = CodingScore.query.filter_by(
        student_email=email
    ).order_by(
        CodingScore.id.desc()
    ).first()

    coding_score = coding.score if coding else 0
    coding_total = coding.total if coding else 0

    if coding and coding.total > 0:
        coding_percent = round(
            (coding.score / coding.total) * 100
        )
    else:
        coding_percent = 0


    # -----------------------------
    # MOCK INTERVIEW
    # -----------------------------

    interview = InterviewScore.query.filter_by(
        student_email=email
    ).order_by(
        InterviewScore.id.desc()
    ).first()

    interview_score = interview.score if interview else 0
    interview_total = interview.total if interview else 0

    if interview and interview.total > 0:
        interview_percent = round(
            (interview.score / interview.total) * 100
        )
    else:
        interview_percent = 0


    # -----------------------------
    # RESUME
    # -----------------------------

    resume_score_record = ResumeScore.query.filter_by(
        student_email=email
    ).first()

    resume_score = (
        resume_score_record.score
        if resume_score_record
        else 0
    )

    resume_total = (
        resume_score_record.total
        if resume_score_record
        else 0
    )

    if resume_score_record and resume_score_record.total > 0:
        resume_percent = round(
            (resume_score_record.score /
             resume_score_record.total) * 100
        )
    else:
        resume_percent = 0


    # -----------------------------
    # OVERALL PROGRESS
    # -----------------------------

    scores = [
        aptitude_percent,
        coding_percent,
        interview_percent,
        resume_percent
    ]

    overall_percent = round(
        sum(scores) / len(scores)
    )


    # -----------------------------
    # SEND DATA TO HTML
    # -----------------------------

    return render_template(
        "progress.html",

        aptitude_score=aptitude_score,
        aptitude_total=aptitude_total,
        aptitude_percent=aptitude_percent,

        coding_score=coding_score,
        coding_total=coding_total,
        coding_percent=coding_percent,

        interview_score=interview_score,
        interview_total=interview_total,
        interview_percent=interview_percent,

        resume_score=resume_score,
        resume_total=resume_total,
        resume_percent=resume_percent,

        overall_percent=overall_percent
    )

@app.route("/readiness")
def readiness():

    if "student_email" not in session:
        return redirect(url_for("login"))

    email = session["student_email"]

    # Latest aptitude score
    aptitude = AptitudeScore.query.filter_by(
        student_email=email
    ).order_by(
        AptitudeScore.id.desc()
    ).first()

    # Latest coding score
    coding = CodingScore.query.filter_by(
        student_email=email
    ).order_by(
        CodingScore.id.desc()
    ).first()

    # Latest interview score
    interview = InterviewScore.query.filter_by(
        student_email=email
    ).order_by(
        InterviewScore.id.desc()
    ).first()

    # Resume score
    resume = ResumeScore.query.filter_by(
        student_email=email
    ).first()

    # Calculate percentages

    aptitude_percent = 0

    if aptitude and aptitude.total > 0:
        aptitude_percent = round(
            (aptitude.score / aptitude.total) * 100
        )

    coding_percent = 0

    if coding and coding.total > 0:
        coding_percent = round(
            (coding.score / coding.total) * 100
        )

    interview_percent = 0

    if interview and interview.total > 0:
        interview_percent = round(
            (interview.score / interview.total) * 100
        )

    resume_percent = 0

    if resume and resume.total > 0:
        resume_percent = round(
            (resume.score / resume.total) * 100
        )

    # Placement readiness
    readiness_score = round(
        (
            aptitude_percent
            + coding_percent
            + interview_percent
            + resume_percent
        ) / 4
    )

    # Prediction
    if readiness_score >= 80:

        prediction = "Excellent"
        message = (
            "You are highly prepared for placement interviews. "
            "Keep maintaining your performance."
        )

    elif readiness_score >= 60:

        prediction = "Good"
        message = (
            "You have good placement readiness. "
            "Continue improving your weaker areas."
        )

    elif readiness_score >= 40:

        prediction = "Average"
        message = (
            "Your preparation is progressing, but you need "
            "more practice before placement interviews."
        )

    else:

        prediction = "Needs Improvement"
        message = (
            "You should focus more on aptitude, coding, "
            "interview preparation and resume improvement."
        )

    return render_template(
        "readiness.html",

        readiness_score=readiness_score,

        aptitude_percent=aptitude_percent,
        coding_percent=coding_percent,
        interview_percent=interview_percent,
        resume_percent=resume_percent,

        level=prediction,
        message=message
    )


@app.route("/check_interviews")
def check_interviews():

    if "student_email" not in session:
        return redirect(url_for("login"))

    records = InterviewScore.query.all()

    result = []

    for record in records:
        result.append({
            "id": record.id,
            "email": record.student_email,
            "score": record.score,
            "total": record.total
        })

    return jsonify(result)


@app.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("login"))


# ----------------------------
# Create Database
# ----------------------------
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)