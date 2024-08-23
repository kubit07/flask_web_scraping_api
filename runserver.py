from api import create_app

app=create_app()

if __name__ == "__main__":
    app.run(host='10.188.201.162', port=5000)