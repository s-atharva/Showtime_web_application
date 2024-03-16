if __name__ == "__main__":
    from web_app import create_app

    app = create_app()
    app.run(port=8005, debug=False)
