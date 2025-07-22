from fastapi import FastAPI, Request
from fastapi import Form, BackgroundTasks
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path
import json
import threading
from dotenv import load_dotenv
import os
import requests

# Load environment variables from .env file
load_dotenv()
app = FastAPI()
file_lock = threading.Lock()  # Create a lock for safe writing

# Mount static files directory
app.mount("/static", StaticFiles(directory="static"), name="static")

# Set up templates directory
templates = Jinja2Templates(directory="templates")

# Serve the index page
@app.get("/", response_class=HTMLResponse)
async def read_index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Route for UPenn
@app.get("/upenn", response_class=HTMLResponse)
async def upenn(request: Request):
    return templates.TemplateResponse("university_page.html", {
        "request": request,
        "university_name": "University of Pennsylvania",
        "university_logo": "/static/assets/upenn_logo.png"
    })

# Route for UTHealth
@app.get("/uthealth", response_class=HTMLResponse)
async def uthealth(request: Request):
    return templates.TemplateResponse("university_page.html", {
        "request": request,
        "university_name": "UTHealth",
        "university_logo": "/static/assets/uthealth_logo.png"
    })

# Route for Yale
@app.get("/yale", response_class=HTMLResponse)
async def yale(request: Request):
    return templates.TemplateResponse("university_page.html", {
        "request": request,
        "university_name": "Yale University",
        "university_logo": "/static/assets/yale_logo.png"
    })

# Route for Iowa
@app.get("/iowa", response_class=HTMLResponse)
async def iowa(request: Request):
    return templates.TemplateResponse("university_page.html", {
        "request": request,
        "university_name": "University of Iowa",
        "university_logo": "/static/assets/iowa_logo.png"
    })


# Route for Mayo
@app.get("/mayo", response_class=HTMLResponse)
async def mayo(request: Request):
    return templates.TemplateResponse("university_page.html", {
        "request": request,
        "university_name": "Mayo Clinic",
        "university_logo": "/static/assets/mayo_logo.png"
    })
    

@app.get("/jhu", response_class=HTMLResponse)
async def jhu(request: Request):
    return templates.TemplateResponse("university_page.html", {
        "request": request,
        "university_name": "Johns Hopkins University",
        "university_logo": "/static/assets/jhu.jpg"
    })

 
@app.get("/wustl", response_class=HTMLResponse)
async def wustl(request: Request):
    return templates.TemplateResponse("university_page.html", {
        "request": request,
        "university_name": "Washington University in St. Louis",
        "university_logo": "/static/assets/WUSTL.png"
    })
@app.get("/pennState", response_class=HTMLResponse)
async def pennState(request: Request):
    return templates.TemplateResponse("university_page.html", {
        "request": request,
        "university_name": "The Pennsylvania State University",
        "university_logo": "/static/assets/PennState.png"
    })   
  

@app.get("/UPitts", response_class=HTMLResponse)
async def UPitts(request: Request):
    return templates.TemplateResponse("university_page.html", {
        "request": request,
        "university_name": "University of Pittsburgh",
        "university_logo": "/static/assets/UPitts.png"
    }) 

@app.get("/pfizer", response_class=HTMLResponse)
async def pfizer(request: Request):
    return templates.TemplateResponse("university_page.html", {
        "request": request,
        "university_name": "Pfizer",
        "university_logo": "/static/assets/pfizer.jpg"
    }) 
@app.get("/UKentucky", response_class=HTMLResponse)
async def UKentucky(request: Request):
    return templates.TemplateResponse("university_page.html", {
        "request": request,
        "university_name": "University of Kentucky",
        "university_logo": "/static/assets/UKentucky.png"
    })
@app.get("/Scripps", response_class=HTMLResponse)
async def Scripps(request: Request):
    return templates.TemplateResponse("university_page.html", {
        "request": request,
        "university_name": "Scripps Research",
        "university_logo": "/static/assets/Scripps.png"
    })
@app.get("/Tufts", response_class=HTMLResponse)
async def Tufts(request: Request):
    return templates.TemplateResponse("university_page.html", {
        "request": request,
        "university_name": "Tufts University",
        "university_logo": "/static/assets/Tufts_University_wordmark.png"
    })
@app.get("/utmb", response_class=HTMLResponse)
async def utmb(request: Request):
    return templates.TemplateResponse("university_page.html", {
        "request": request,
        "university_name": "The University of Texas Medical Branch",
        "university_logo": "/static/assets/utmb-logo.png"
    })   
@app.get("/others", response_class=HTMLResponse)
async def others(request: Request):
    return templates.TemplateResponse("university_page.html", {
        "request": request,
        "university_name": "Other Institutions",
        "university_logo": "/static/assets/institution4.png"
    })

@app.get("/ai-chat")
async def ai_chat_interface():
    """Serve the AI chat interface"""
    return templates.TemplateResponse("ai_chat_interface.html", {"request": {}})

# Get real count stats data
STATS_FILE = "stats.json"

# Function to read statistics
def read_stats():
    stats_path = Path(STATS_FILE)
    if not stats_path.exists():
        return {"userCount": 0, "conversationCount": 0}

    with open(STATS_FILE, "r") as f:
        return json.load(f)

# Function to safely update statistics with file locking
def update_stats(key):
    with file_lock:  # Lock the file to prevent race conditions
        stats = read_stats()
        stats[key] = stats.get(key, 0) + 1  # Safely increment

        with open(STATS_FILE, "w") as f:
            json.dump(stats, f, indent=4)

    return stats[key]

@app.post("/track-user/")
def track_user():
    return {"userCount": update_stats("userCount")}

@app.post("/track-conversation/")
def track_conversation():
    return {"conversationCount": update_stats("conversationCount")}

@app.get("/get-stats/")
def get_stats():
    return read_stats()



FEEDBACK_API_KEY = os.getenv("FEEDBACK_API_KEY")

# Function to send email using SendGrid's Python library
def send_feedback_email(feedback):
    print("Starting email send task...")  # Debugging

    url = "https://dify-service-765428358644.us-central1.run.app/v1/workflows/run"
    headers = {
        "Authorization": f"Bearer {FEEDBACK_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "inputs": { "content": json.dumps(feedback) },
        "response_mode": "streaming",
        "user": "shawn"
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        
        print(f"Email sent! Status: {response.status_code}")
    except Exception as e:
        print(f"Failed to send email: {str(e)}")


@app.post("/submit-feedback/")
async def submit_feedback(navigation: str = Form(...), chatbot: str = Form(...), 
                          rating: str = Form(...), suggestions: str = Form(None)):
    feedback_dict = {
    "Was it easy to navigate the website?": navigation,
    "Did the chatbot provide useful solutions?": chatbot,
    "How would you rate your experience?": f"{rating} star",
    "Suggestions": suggestions if suggestions else "No additional feedback"
}

    print("Running email function synchronously for debugging...")
    send_feedback_email(feedback_dict)  # Run directly

    return {"message": "Feedback sent successfully!"}