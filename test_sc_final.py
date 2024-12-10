import unittest
from unittest import mock
from unittest.mock import patch, MagicMock
import sqlite3
from sc_final import App
class TestApp(unittest.TestCase):
    def setUp(self):
        self.app = App()
        self.app.create_sqlite3 = MagicMock()
        self.app.conn = sqlite3.connect(":memory:")
        self.app.cursor = self.app.conn.cursor()
        self.app.create_sqlite3()

        self.patcher = patch('tkinter.messagebox')
        self.mock_messagebox = self.patcher.start()

    def tearDown(self):
        self.patcher.stop()
        self.app.conn.close()

    def test_create_sqlite3(self):
        """Tests if the userTable is created successfully."""
        self.app.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='userTable';")
        table = self.app.cursor.fetchone()
        self.assertIsNotNone(table)
        self.assertEqual(table[0], 'userTable')

    def test_usr_sign_up_success(self):
        """Tests successful user registration."""
        self.app.usernameEntry = MagicMock()
        self.app.passwordEntry = MagicMock()
        self.app.okPasswordEntry = MagicMock()

        self.app.usernameEntry.get.return_value = 'testuser'
        self.app.passwordEntry.get.return_value = 'password123'
        self.app.okPasswordEntry.get.return_value = 'password123'

        self.app.registerWindows = MagicMock()

        with patch('tkinter.messagebox.showinfo'):
            self.app.usr_sign_up()

    def test_usr_sign_up_duplicate_username(self):
        """Tests registration with an existing username."""
        self.app.cursor.execute("INSERT INTO userTable(username, password) VALUES (?, ?)", ('testuser', 'password123'))
        self.app.conn.commit()

        self.app.usernameEntry = MagicMock()
        self.app.passwordEntry = MagicMock()
        self.app.okPasswordEntry = MagicMock()

        self.app.usernameEntry.get.return_value = 'testuser'
        self.app.passwordEntry.get.return_value = 'password123'
        self.app.okPasswordEntry.get.return_value = 'password123'

        with patch('tkinter.messagebox.showwarning'):
            self.app.usr_sign_up()

    def test_usr_sign_up_empty_fields(self):
        """Tests registration with empty username or password."""
        self.app.usernameEntry = MagicMock()
        self.app.passwordEntry = MagicMock()
        self.app.okPasswordEntry = MagicMock()

        self.app.usernameEntry.get.return_value = ''
        self.app.passwordEntry.get.return_value = ''
        self.app.okPasswordEntry.get.return_value = ''

        with patch('tkinter.messagebox.showerror'):
            self.app.usr_sign_up()

    def test_usr_sign_up_password_mismatch(self):
        """Tests registration when password and confirmation do not match."""
        self.app.usernameEntry = MagicMock()
        self.app.passwordEntry = MagicMock()
        self.app.okPasswordEntry = MagicMock()

        self.app.usernameEntry.get.return_value = 'testuser'
        self.app.passwordEntry.get.return_value = 'password123'
        self.app.okPasswordEntry.get.return_value = 'password456'

        with patch('tkinter.messagebox.showerror'):
            self.app.usr_sign_up()

    def test_usr_log_in_success(self):
        """Tests successful login."""
        self.app.cursor.execute("INSERT INTO userTable(username, password) VALUES (?, ?)", ('testuser', 'password123'))
        self.app.conn.commit()

        self.app.entry_usr_name = MagicMock()
        self.app.entry_usr_pwd = MagicMock()
        self.app.entry_usr_name.get.return_value = 'testuser'
        self.app.entry_usr_pwd.get.return_value = 'password123'

        with patch('tkinter.messagebox.showinfo') as mock_showinfo, \
             patch('Function') as mock_Function:
            instance_Function = mock_Function.return_value
            self.app.usr_log_in()
            mock_showinfo.assert_called_with(title='Welcome!', message='Welcome testuser')
            self.assertEqual(self.app.usr_name, 'testuser')
            self.assertFalse(self.app.flag)
            mock_Function.assert_called_with(self.app)

    def test_usr_log_in_wrong_password(self):
        """Tests login with a wrong password."""
        self.app.cursor.execute("INSERT INTO userTable(username, password) VALUES (?, ?)", ('testuser', 'password123'))
        self.app.conn.commit()

        self.app.entry_usr_name = MagicMock()
        self.app.entry_usr_pwd = MagicMock()
        self.app.entry_usr_name.get.return_value = 'testuser'
        self.app.entry_usr_pwd.get.return_value = 'wrongpassword'

        with patch('tkinter.messagebox.showinfo') as mock_showinfo:
            self.app.usr_log_in()
            mock_showinfo.assert_called_with(title='ERROR', message="WRONG PASSWORD")

    def test_usr_log_in_empty_fields(self):
        """Tests login with empty username or password."""
        self.app.entry_usr_name = MagicMock()
        self.app.entry_usr_pwd = MagicMock()
        self.app.entry_usr_name.get.return_value = ''
        self.app.entry_usr_pwd.get.return_value = ''

        with patch('tkinter.messagebox.showerror') as mock_showerror:
            self.app.usr_log_in()

    def test_usr_log_in_no_users(self):
        """Tests login when no users exist, expecting a signup prompt."""
        self.app.entry_usr_name = MagicMock()
        self.app.entry_usr_pwd = MagicMock()
        self.app.entry_usr_name.get.return_value = 'newuser'
        self.app.entry_usr_pwd.get.return_value = 'password123'

        with patch('tkinter.messagebox.askyesno') as mock_askyesno, \
             patch.object(self.app, 'usr_sign_up') as mock_usr_sign_up:
            mock_askyesno.return_value = True
            self.app.usr_log_in()
            mock_askyesno.assert_called_with('Welcome!', 'You have not registered yet, do you want to register now?')
            mock_usr_sign_up.assert_called()

    def test_AddPatInfo_success(self):
        """Tests successfully adding patient info."""
        self.app.cursor.execute = MagicMock()
        self.app.conn.commit = MagicMock()

        self.app.patIdEntry = MagicMock()
        self.app.nameEntry = MagicMock()
        self.app.TypeOfDiseaseEntry = MagicMock()
        self.app.RecoveryTimeEntry = MagicMock()

        self.app.patIdEntry.get.return_value = 'P001'
        self.app.nameEntry.get.return_value = 'John Doe'
        self.app.TypeOfDiseaseEntry.get.return_value = 'Flu'
        self.app.RecoveryTimeEntry.get.return_value = '7'

        with patch('tkinter.messagebox.showinfo'):
            self.app.AddPatInfo()

    def test_AddPatInfo_duplicate_patId(self):
        """Tests adding patient info with an existing patient ID."""
        self.app.cursor.execute = MagicMock()
        self.app.cursor.fetchall.return_value = [('P001', 'John Doe', 'Flu', 7.0)]

        self.app.patIdEntry = MagicMock()
        self.app.nameEntry = MagicMock()
        self.app.TypeOfDiseaseEntry = MagicMock()
        self.app.RecoveryTimeEntry = MagicMock()

        self.app.patIdEntry.get.return_value = 'P001'
        self.app.nameEntry.get.return_value = 'John Doe'
        self.app.TypeOfDiseaseEntry.get.return_value = 'Flu'
        self.app.RecoveryTimeEntry.get.return_value = '7'

        with patch('tkinter.messagebox.showwarning'):
            self.app.AddPatInfo()

if __name__ == '__main__':
    unittest.main()
