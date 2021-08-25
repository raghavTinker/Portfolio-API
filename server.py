import uvicorn
if __name__ == "__main__":
    uvicorn.run("app.main:app", 
                host="192.168.1.102", 
                port=6000,
                reload=True,
                ssl_keyfile="./raghavtinker.servatom.com-key.pem",
                ssl_certfile="./raghavtinker.servatom.com.pem"
                )