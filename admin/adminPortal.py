import uvicorn
if __name__ == "__main__":
    uvicorn.run("admin.admin:app",
                host="0.0.0.0",
                port=4000,
                reload=True,
                )
