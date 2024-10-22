import sqlite3

class BrandRegistration:

    def __init__(self, db_name='brands.db'):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS brands (
                id INTEGER PRIMARY KEY,
                uuid TEXT NOT NULL UNIQUE,
                brand_name TEXT NOT NULL,
                brand_tagline TEXT,
                industry TEXT,
                brand_description TEXT,
                primary_color TEXT,
                secondary_color TEXT,
                complementary_color TEXT,
                brand_keywords TEXT
            )
        ''')
        self.conn.commit()

    def add_data(self, uuid, brand_name, brand_tagline, industry, brand_description,
                 primary_color, secondary_color, complementary_color, brand_keywords):
        try:
            self.cursor.execute('''
                INSERT INTO brands (uuid, brand_name, brand_tagline, industry, brand_description,
                                    primary_color, secondary_color, complementary_color, brand_keywords)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (uuid, brand_name, brand_tagline, industry, brand_description,
                  primary_color, secondary_color, complementary_color, brand_keywords))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def delete_data(self, uuid):
        self.cursor.execute('DELETE FROM brands WHERE uuid=?', (uuid,))
        self.conn.commit()
        return self.cursor.rowcount > 0

    def edit_data(self, uuid, **kwargs):
        updates = []
        values = []
        for key, value in kwargs.items():
            updates.append(f"{key} = ?")
            values.append(value)
        values.append(uuid)
        update_query = f"UPDATE brands SET {', '.join(updates)} WHERE uuid = ?"
        self.cursor.execute(update_query, values)
        self.conn.commit()
        return self.cursor.rowcount > 0

    def close_connection(self):
        self.conn.close()

if __name__ == "__main__":
    pass
    # brand_manager = BrandRegistration()
    
    # # Adding a brand
    # success = brand_manager.add_data(
    #     brand_name="Tech Innovators",
    #     brand_tagline="Innovating the Future",
    #     industry="Technology",
    #     brand_description="A leading tech company focusing on innovative solutions.",
    #     primary_color="#FF5733",
    #     secondary_color="#C70039",
    #     complementary_color="#FFC300",
    #     brand_keywords="technology, innovation, future"
    # )
    # print("Brand added:", success)

    # # Editing a brand
    # success = brand_manager.edit_data("some-uuid", brand_tagline="Shaping Tomorrow")  # Replace with a valid UUID
    # print("Brand updated:", success)

    # # Deleting a brand
    # success = brand_manager.delete_data("some-uuid")  # Replace with a valid UUID
    # print("Brand deleted:", success)

    # # Closing connection
    # brand_manager.close_connection()