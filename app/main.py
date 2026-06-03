"""
app/main.py — entry point for the FastAPI application

*  Registers all 8 routers (auth + 7 agents).
*  Sets up CORS middleware to allow frontend access.
*  /health endpoint for quick uptime checks.
*  Servers static/idex.html at root /. for quick manual testing in the browser.

"""