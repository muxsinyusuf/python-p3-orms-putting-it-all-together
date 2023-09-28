import sqlite3

CONN = sqlite3.connect('lib/dogs.db')
CURSOR = CONN.cursor()

class Dog:
    def __init__(self, name, breed):
        self.name = name
        self.breed = breed
    
    @classmethod
    def create_table(cls):
        sql = """
            CREATE TABLE IF NOT EXISTS dogs (
                id INTEGER PRIMARY KEY,
                name TEXT,
                breed TEXT
            )
        """
        CURSOR.execute(sql)
    
    @classmethod
    def drop_table(cls):
        sql = """
            DROP TABLE IF EXISTS dogs
        """
        CURSOR.execute(sql)
    
    def save(self):
        sql = """
            INSERT INTO dogs (name, breed)
            VALUES (?, ?)
        """
        CURSOR.execute(sql, (self.name, self.breed))
        CONN.commit()
    
    @classmethod
    def get_all(cls):
        sql = """
            SELECT *
            FROM dogs
        """
        all_dogs = CURSOR.execute(sql).fetchall()
        return [cls(*row) for row in all_dogs]
    
    @classmethod
    def create(cls, name, breed):
        new_dog = cls(name, breed)
        new_dog.save()
        return new_dog
    
    @classmethod
    def new_from_db(cls, db_row):
        name, breed = db_row[1], db_row[2]
        return cls(name, breed)
    
    @classmethod
    def find_by_name(cls, name):
        sql = """
            SELECT *
            FROM dogs
            WHERE name = ?
        """
        result = CURSOR.execute(sql, (name,)).fetchone()
        if result:
            return cls.new_from_db(result)
        else:
            return None
    
    @classmethod
    def find_by_id(cls, dog_id):
        sql = """
            SELECT *
            FROM dogs
            WHERE id = ?
        """
        result = CURSOR.execute(sql, (dog_id,)).fetchone()
        if result:
            return cls.new_from_db(result)
        else:
            return None

if __name__ == "__main__":
    Dog.drop_table()  
    Dog.create_table()
    
   
    new_dog = Dog.create("Fido", "Labrador Retriever")
    
    all_dogs = Dog.get_all()
    for dog in all_dogs:
        print(f"Dog: {dog.name}, Breed: {dog.breed}")
    
    dog_by_name = Dog.find_by_name("Fido")
    if dog_by_name:
        print("Dog found by name:", dog_by_name.name, dog_by_name.breed)
    else:
        print("No dog found with that name")
    
    dog_by_id = Dog.find_by_id(1)  
    if dog_by_id:
        print("Dog found by ID:", dog_by_id.name, dog_by_id.breed)
    else:
        print("No dog found with that ID")
