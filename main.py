from typing import Annotated, Optional
from fastapi import Cookie, Depends, FastAPI, Form, status
from fastapi.exceptions import RequestValidationError
from fastapi.requests import Request
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse, Response
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import auth_manager
import crud
from models import UserInDB

app = FastAPI()

# Serve static files like CSS, JS, images, etc. if needed
app.mount("/static", StaticFiles(directory="static"), name="static")

# Set up templates directory
templates = Jinja2Templates(directory="templates")

# Exception Handler
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(status_code=400, content={"detail": "Invalid input. Please check your data and try again."})

############# HTML RENDER ##############
########################################
# Public page when no logged in
@app.get("/", response_class=HTMLResponse)
async def public_page(request: Request):
    return templates.TemplateResponse(request, "public.html")

# Form to register a New User
@app.get("/signup/", response_class=HTMLResponse)
async def signup_page(request: Request):
    return templates.TemplateResponse(request, "signup.html")

# Form to Login a User
@app.get("/login/", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse(request, "login.html")

@app.get("/dashboard")
async def dash_page(request: Request, session_token: Optional[str] = Cookie(None)):
    if session_token:
        user = auth_manager.check_permissions(session_token)
        return templates.TemplateResponse(request, "dashboard.html", context={"user": user.full_name})
    return templates.TemplateResponse(request, "login.html")

############# POST FORMS ###############
########################################
# Register a New User
@app.post("/signup/")
async def register_user(request: Request,
                        email: Annotated[str, Form()],
                        full_name: Annotated[str, Form()],
                        password: Annotated[str, Form()],
                        retyped_password: Annotated[str, Form()]):

    # Verify there is not user registered with same emial address
    error_messsage = None
    normalize_email = email.strip().lower()
    existing_user_dict = crud.search_user(normalize_email)
    if existing_user_dict:
        error_messsage = "This email already exist."

    # Verify that the user didnt misstype the password
    if password != retyped_password:
        error_messsage = "Passwords doesn't match."

    if error_messsage:
        return templates.TemplateResponse(request, "signup.html", context={"error_messsage": error_messsage})

    # Sanitize and Validate User inputs
    new_user = UserInDB(email=normalize_email,
                        full_name=full_name,
                        password=auth_manager.get_password_hash(password))

    # Prepare data input and save on DB, the redirect to Login page
    new_user_dict = new_user.model_dump()
    if crud.create_user(new_user_dict):
        return templates.TemplateResponse(request,
                                          "login.html",
                                          context={"success_message": "Registration successful. You can now log in."})
    else:
        return templates.TemplateResponse(request,
                                          "login.html",
                                          context={"error_messsage": "Registration failed. Please try again later."})


# Get token by providing username and password
@app.post("/token")
async def get_token(request: Request,
                    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    # Find user if exist
    user = auth_manager.authenticate_user(form_data.username, form_data.password)
    if not user:
        return templates.TemplateResponse(request,
                                          "login.html",
                                          context={"error_messsage": "Incorrect username or password"})

    # Create session Token
    session_token = auth_manager.encrypt_user(user.email)

    # Redirect to main page and set session cookie on response
    response = RedirectResponse(url="/dashboard", status_code=status.HTTP_302_FOUND)
    response.set_cookie(key="session_token", value=session_token, httponly=True)
    return response


@app.post("/logout")
async def logout(response: Response):
    response = RedirectResponse(url="/", status_code=status.HTTP_302_FOUND)
    response.delete_cookie("session_token")
    return response