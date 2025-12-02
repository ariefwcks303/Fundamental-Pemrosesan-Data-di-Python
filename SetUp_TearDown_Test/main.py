import unittest
 
class UserDatabase:
    def __init__(self):
        # Simulasi database dengan tipe data dictionary
        self.users = {}

    def add_user(self, user_id, name):
        if user_id in self.users:
            raise ValueError("User already exists")
        self.users[user_id] = name

    def remove_user(self, user_id):
        if user_id in self.users:
            del self.users[user_id]

    def get_user(self, user_id):
        return self.users.get(user_id)


class TestUserDatabase(unittest.TestCase):

    def setUp(self):
        # Method ini dijalankan setiap sebelum pengujian
        # Membuat instance database pengguna baru untuk setiap pengujian
        self.db = UserDatabase()

        # Menambahkan data pengguna awal sebagai persiapan
        self.db.add_user(1, "Alice")
        self.db.add_user(2, "Bob")

    def tearDown(self):
        # Method ini dijalankan setelah setiap pengujian
        # Membersihkan database pengguna (simulasi)
        self.db = None

    def test_add_user(self):
        # Menguji penambahan pengguna baru
        self.db.add_user(3, "Charlie")
        self.assertEqual(self.db.get_user(3), "Charlie")

    def test_remove_user(self):
        # Menguji penghapusan pengguna
        self.db.remove_user(1)
        self.assertIsNone(self.db.get_user(1))

    def test_get_existing_user(self):
        # Menguji mendapatkan data pengguna yang sudah ada
        self.assertEqual(self.db.get_user(1), "Alice")
        self.assertEqual(self.db.get_user(2), "Bob")

    def test_add_existing_user_raises_error(self):
        # Menguji penambahan pengguna yang sudah ada dan memunculkan error
        with self.assertRaises(ValueError):
            self.db.add_user(1, "Alice Duplicate")

if __name__ == "__main__":
    unittest.main()