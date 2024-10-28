# main.py

from views.login_view import LoginView

def main():
    app = LoginView()
    app.run()

if __name__ == '__main__':
    main()
