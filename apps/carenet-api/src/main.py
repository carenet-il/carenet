if __name__ == "__main__":
    import uvicorn, sys, os
    from dotenv import load_dotenv

    
    load_dotenv()
    # to allow import from libs
    sys.path.append(os.path.join(os.path.dirname(__file__), "..", "..", ".."))

    if os.getenv("ENV") == "dev":
        uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
    else:
        uvicorn.run("app:app", host="0.0.0.0", port=8000, workers=2)
