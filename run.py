from app import create_app

app = create_app()


@app.route('/')
def index():
    return "天下莫柔弱于水，而攻坚强者莫之能胜，以其无以易之。"


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
