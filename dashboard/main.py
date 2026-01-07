from fastapi import FastAPI, Request, Form, Response, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from db import save_review, get_reviews, update_analysis
from generate import get_gemini_response
from prompts import get_analysis_prompt
import json
import os
import uvicorn

app = FastAPI()

# 1. SETUP: Templates & Static Files
templates = Jinja2Templates(directory="templates")
if not os.path.exists("static"): 
    os.makedirs("static")
app.mount("/static", StaticFiles(directory="static"), name="static")

# 2. CONFIG: Admin Credentials & Security
COOKIE_NAME = "admin_session"
ADMIN_USER = os.environ.get("ADMIN_USER", "admin")
ADMIN_PASS = os.environ.get("ADMIN_PASS", "admin123")

# ==========================================
#  CLIENT ROUTES (The Public Form)
# ==========================================

@app.get("/", response_class=HTMLResponse)
async def form(request: Request):
    """Renders the public feedback form."""
    return templates.TemplateResponse("client.html", {"request": request, "success": False})

@app.post("/submit", response_class=HTMLResponse)
async def submit(request: Request, name: str = Form(...), review: str = Form(...), rating: int = Form(...)):
    """Handles form submission and saves to DB."""
    save_review(name, review, rating)
    return templates.TemplateResponse("client.html", {"request": request, "success": True})


# ==========================================
#  AUTH ROUTES (Login/Logout)
# ==========================================

@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    """Renders the login page."""
    return templates.TemplateResponse("login.html", {"request": request, "error": None})

@app.post("/login", response_class=HTMLResponse)
async def login_submit(request: Request, response: Response, username: str = Form(...), password: str = Form(...)):
    """Validates credentials and sets the session cookie."""
    if username == ADMIN_USER and password == ADMIN_PASS:
        # Success: Redirect to dashboard with a cookie
        response = RedirectResponse(url="/admin", status_code=status.HTTP_303_SEE_OTHER)
        response.set_cookie(key=COOKIE_NAME, value="authenticated", httponly=True)
        return response
    else:
        # Failure: Show error on login page
        return templates.TemplateResponse("login.html", {"request": request, "error": "Invalid username or password"})

@app.get("/logout")
async def logout(response: Response):
    """Clears the session cookie."""
    response = RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)
    response.delete_cookie(COOKIE_NAME)
    return response


# ==========================================
#  ADMIN ROUTES (The Dashboard)
# ==========================================

@app.get("/admin", response_class=HTMLResponse)
async def dashboard(request: Request):
    """
    Renders the protected Admin Dashboard.
    Also triggers Lazy AI Analysis for new reviews.
    """
    # 1. SECURITY CHECK: Ensure user is logged in
    session_token = request.cookies.get(COOKIE_NAME)
    if session_token != "authenticated":
        return RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)

    # 2. FETCH DATA
    reviews = get_reviews()
    
    # 3. AI PROCESSING (Lazy Load)
    updated_data = False
    for r in reviews:
        if r['analysis'] is None:
            print(f"🧠 AI Processing Review #{r['id']}...")
            try:
                # Generate Prompt & Call Gemini
                prompt = get_analysis_prompt(r['text'])
                response = get_gemini_response(prompt)
                
                # Parse JSON safely
                clean_json = response.replace("```json", "").replace("```", "").strip()
                analysis = json.loads(clean_json)
            except Exception as e:
                print(f"❌ Error analyzing review {r['id']}: {e}")
                analysis = {
                    "sentiment": "Error",
                    "summary": "Analysis Failed",
                    "tags": ["Error"],
                    "action_item": "Check API Keys/Logs"
                }
            
            # Update DB
            update_analysis(r['id'], analysis)
            updated_data = True
            
    # Refresh data if we just updated it
    if updated_data:
        reviews = get_reviews()
        
    return templates.TemplateResponse("admin.html", {"request": request, "reviews": reviews})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)