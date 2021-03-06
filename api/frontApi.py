import uvicorn
if __name__ == "__main__":
    uvicorn.run("api.main:app", 
                host="0.0.0.0", 
                port=5000,
                reload=True,
                ssl_keyfile="./raghavtinker.servatom.com-key.pem",
                ssl_certfile="./raghavtinker.servatom.com.pem"
                )