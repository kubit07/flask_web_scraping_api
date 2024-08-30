from api import create_app

app=create_app()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000) #changer les 0.0.0.0 par l'adresse Ip de votre machine

