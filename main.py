from PySide6.QtWidgets import QApplication
import sys

from viewmodels.auth.create_account_viewmodel import CreateAccountViewModel
from views.auth.create_account_view import CreateAccountView

from data.database import SessionLocal, init_db

from views.auth.login_view import LoginView
from viewmodels.auth.login_viewmodel import LoginViewModel
if __name__ == "__main__":
    init_db()
    app = QApplication(sys.argv)

    db_session = SessionLocal()    

    # vm = CreateAccountViewModel(db_session)
    # win = CreateAccountView(vm)
    vm = LoginViewModel(db_session)
    win = LoginView(vm)

    win.show()

    sys.exit(app.exec())

    