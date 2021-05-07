import sqlite3


def add_user(user_id, firstname, lastname):
    try:
        sqlite_connection = sqlite3.connect('BeautyBotBase.db')
        cursor = sqlite_connection.cursor()
        sqlite_insert_query = """INSERT INTO Users VALUES(?,?,?)"""
        cursor.execute(sqlite_insert_query, (user_id, firstname, lastname))
        sqlite_connection.commit()
        cursor.close()
    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()


def add_empty_user_to_clothes_temp(id_user, id_photo):
    try:
        sqlite_connection = sqlite3.connect('BeautyBotBase.db')
        cursor = sqlite_connection.cursor()
        sqlite_insert_query = """INSERT INTO ClothesTemp(IdUser,IdPhoto,GenderType,SeasonType,Category,CategoryType, Color,Name) VALUES(?,?,?,?,?,?,?,?)"""
        cursor.execute(sqlite_insert_query, (id_user, id_photo, None, None, None, None, None, None))
        sqlite_connection.commit()
        cursor.close()
    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()


def get_photo_path(id_photo):
    try:
        sqlite_connection = sqlite3.connect('BeautyBotBase.db')
        cursor = sqlite_connection.cursor()
        sqlite_select_query = """Select FilePath FROM Photos WHERE IdPhoto = ?"""
        cursor.execute(sqlite_select_query, (id_photo,))
        return str(cursor.fetchall()[0][0])
    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()


def update_clothes_temp_table_gender_type(id_photo, gender_type):
    try:
        sqlite_connection = sqlite3.connect('BeautyBotBase.db')
        cursor = sqlite_connection.cursor()
        sqlite_update_query = """UPDATE ClothesTemp SET GenderType = ? where IdPhoto = ?"""
        cursor.execute(sqlite_update_query, (gender_type, id_photo))
        sqlite_connection.commit()
        cursor.close()
    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()


def update_clothes_temp_table_season_type(id_photo, season_type):
    try:
        sqlite_connection = sqlite3.connect('BeautyBotBase.db')
        cursor = sqlite_connection.cursor()
        sqlite_update_query = """UPDATE ClothesTemp SET SeasonType = ? where IdPhoto = ?"""
        cursor.execute(sqlite_update_query, (season_type, id_photo))
        sqlite_connection.commit()
        cursor.close()
    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()


def update_clothes_temp_table_category(id_photo, category):
    try:
        sqlite_connection = sqlite3.connect('BeautyBotBase.db')
        cursor = sqlite_connection.cursor()
        sqlite_update_query = """UPDATE ClothesTemp SET Category = ? where IdPhoto = ?"""
        print((category, id_photo))
        cursor.execute(sqlite_update_query, (category, id_photo))
        sqlite_connection.commit()
        cursor.close()
    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()


def update_clothes_temp_table_category_type(id_photo, category_type):
    try:
        sqlite_connection = sqlite3.connect('BeautyBotBase.db')
        cursor = sqlite_connection.cursor()
        sqlite_update_query = """UPDATE ClothesTemp SET CategoryType = ? where IdPhoto = ?"""
        cursor.execute(sqlite_update_query, (category_type, id_photo))
        sqlite_connection.commit()
        cursor.close()
    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()


def update_clothes_temp_table_color(id_photo, color):
    try:
        sqlite_connection = sqlite3.connect('BeautyBotBase.db')
        cursor = sqlite_connection.cursor()
        sqlite_update_query = """UPDATE ClothesTemp SET Color = ? where IdPhoto = ?"""
        cursor.execute(sqlite_update_query, (color, id_photo))
        sqlite_connection.commit()
        cursor.close()
    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()


def update_clothes_temp_table_name(id_photo, name):
    try:
        sqlite_connection = sqlite3.connect('BeautyBotBase.db')
        cursor = sqlite_connection.cursor()
        sqlite_update_query = """UPDATE ClothesTemp SET Name = ? where IdPhoto = ?"""
        cursor.execute(sqlite_update_query, (name, id_photo))
        sqlite_connection.commit()
        cursor.close()
    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()

def add_photo(user_id, file_path):
    try:
        sqlite_connection = sqlite3.connect('BeautyBotBase.db')
        cursor = sqlite_connection.cursor()
        sqlite_insert_query = """INSERT INTO Photos(IdUser,FilePath) VALUES(?,?)"""
        cursor.execute(sqlite_insert_query, (user_id, file_path))
        sqlite_connection.commit()
        cursor.close()
    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()


def get_last_created_photo_id(id_user):
    try:
        sqlite_connection = sqlite3.connect('BeautyBotBase.db')
        cursor = sqlite_connection.cursor()
        sqlite_select_query = """SELECT IdPhoto FROM Photos where IdUser = ? ORDER BY IdPhoto DESC LIMIT 1"""
        cursor.execute(sqlite_select_query, (id_user,))
        return int(cursor.fetchall()[0][0])
    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()


def is_user_registered(id_user):
    try:
        sqlite_connection = sqlite3.connect('BeautyBotBase.db')
        cursor = sqlite_connection.cursor()
        sqlite_select_query = """SELECT IdUser FROM Users WHERE IdUser = ?"""
        cursor.execute(sqlite_select_query, (id_user,))
        if len(cursor.fetchall()) == 1:
            return True
        else:
            return False
    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()


def transport_from_temp_clothes_to_clothes(id_photo):
    try:
        sqlite_connection = sqlite3.connect('BeautyBotBase.db')
        cursor = sqlite_connection.cursor()
        cursor.execute("Select * from ClothesTemp")
        print(cursor.fetchall())
        sqlite_insert_query = """INSERT INTO Clothes(IdUser,IdPhoto,GenderType,SeasonType,Category,CategoryType,Color, Name)
                          SELECT IdUser,IdPhoto,GenderType,SeasonType,Category,CategoryType, Color, Name FROM ClothesTemp
                          WHERE IdPhoto = ?
                            """
        cursor.execute(sqlite_insert_query, (id_photo, ))
        sqlite_connection.commit()
        cursor.close()
    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()


def delete_clothes_from_clothes_temp(id_photo):
    try:
        sqlite_connection = sqlite3.connect('BeautyBotBase.db')
        cursor = sqlite_connection.cursor()
        sqlite_delete_query = """DELETE FROM ClothesTemp WHERE IdPhoto = ?"""
        cursor.execute(sqlite_delete_query, (id_photo,))
        sqlite_connection.commit()
        cursor.close()
    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()


def delete_look(id_look):
    try:
        sqlite_connection = sqlite3.connect('BeautyBotBase.db')
        cursor = sqlite_connection.cursor()
        sqlite_delete_query = """DELETE FROM Looks WHERE IdLook = ?"""
        cursor.execute(sqlite_delete_query, (id_look,))
        sqlite_connection.commit()
        cursor.close()
    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()


def delete_look_input_status(id_look):
    try:
        sqlite_connection = sqlite3.connect('BeautyBotBase.db')
        cursor = sqlite_connection.cursor()
        sqlite_delete_query = """DELETE FROM LookInputStatus WHERE IdLookInputStatus = ?"""
        cursor.execute(sqlite_delete_query, (id_look,))
        sqlite_connection.commit()
        cursor.close()
    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()


def get_clothes(id_user, category = None, category_type = None):
    try:
        sqlite_connection = sqlite3.connect('BeautyBotBase.db')
        cursor = sqlite_connection.cursor()
        if category is None and category_type is None:
            sqlite_select_query = """SELECT * FROM Clothes WHERE IdUser = ?"""
            cursor.execute(sqlite_select_query, (id_user, ))
        else:
            sqlite_select_query = """SELECT * FROM Clothes WHERE IdUser = ? AND Category = ? AND CategoryType = ?"""
            cursor.execute(sqlite_select_query, (id_user, category, category_type))
        return cursor.fetchall()
    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()


def create_empty_look_insert_state_table(id_look):
    try:
        sqlite_connection = sqlite3.connect('BeautyBotBase.db')
        cursor = sqlite_connection.cursor()
        sqlite_insert_query = """INSERT INTO LookInputStatus(IdLookInputStatus,
                                                             IsHeadCategotyInserted,
                                                             IsTopCategotyInserted,
                                                             IsBottomCategotyInserted,
                                                             IsFootwearCategoryInserted,
                                                             IsAccesoryCategoryInserted) 
                                                             VALUES(?,?,?,?,?,?)"""
        cursor.execute(sqlite_insert_query, (id_look, "0", "0", "0", "0", "0"))
        sqlite_connection.commit()
        cursor.close()
    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()


def set_look_state(id_look, category_type):
    try:
        sqlite_connection = sqlite3.connect('BeautyBotBase.db')
        cursor = sqlite_connection.cursor()
        sqlite_update_query = """"""
        if category_type == "head":
            sqlite_update_query = """UPDATE LookInputStatus SET IsHeadCategotyInserted = 1 WHERE IdLookInputStatus = ?"""
        elif category_type == "top":
            sqlite_update_query = """UPDATE LookInputStatus SET IsTopCategotyInserted = 1 WHERE IdLookInputStatus = ?"""
        elif category_type == "bottom":
            sqlite_update_query = """UPDATE LookInputStatus SET IsBottomCategotyInserted = 1 WHERE IdLookInputStatus = ?"""
        elif category_type == "footwear":
            sqlite_update_query = """UPDATE LookInputStatus SET IsFootwearCategoryInserted = 1 WHERE IdLookInputStatus = ?"""
        elif category_type == "accessory":
            sqlite_update_query = """UPDATE LookInputStatus SET IsAccesoryCategoryInserted = 1 WHERE IdLookInputStatus = ?"""
        cursor.execute(sqlite_update_query, (id_look,))
        sqlite_connection.commit()
        cursor.close()
    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()

def is_look_inserted(id_user):
    try:
        sqlite_connection = sqlite3.connect('BeautyBotBase.db')
        cursor = sqlite_connection.cursor()
        sqlite_select_query ="""SELECT IdLookInputStatus FROM LookInputStatus 
                                 WHERE IdLookInputStatus = ? AND
                                 IsHeadCategotyInserted = 1 AND
                                 IsTopCategotyInserted = 1 AND
                                 IsBottomCategotyInserted = 1 AND
                                 IsFootwearCategoryInserted = 1 AND
                                 IsAccesoryCategoryInserted =1 
                                 """
        cursor.execute(sqlite_select_query, (id_user,))
        if len(cursor.fetchall()) == 1:
            return True
        else:
            return False
    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()

def is_add_look_for_user_proccesed(id_user):
    try:
        sqlite_connection = sqlite3.connect('BeautyBotBase.db')
        cursor = sqlite_connection.cursor()
        sqlite_select_query = """SELECT IdLookInputStatus FROM LookInputStatus WHERE IdLookInputStatus = ?"""
        cursor.execute(sqlite_select_query, (id_user,))
        if len(cursor.fetchall()) == 1:
            return True
        else:
            return False
    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()


def create_emtpy_look(name, id_user):
    try:
        sqlite_connection = sqlite3.connect('BeautyBotBase.db')
        cursor = sqlite_connection.cursor()
        sqlite_insert_query = """INSERT INTO Looks VALUES(?,?,?)"""
        cursor.execute(sqlite_insert_query, (None, id_user, name))
        sqlite_connection.commit()
        cursor.close()
    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()


def get_last_created_look_id(id_user):
    try:
        sqlite_connection = sqlite3.connect('BeautyBotBase.db')
        cursor = sqlite_connection.cursor()
        sqlite_select_query = """SELECT IdLook FROM Looks where IdUser = ? ORDER BY IdLook DESC LIMIT 1"""
        cursor.execute(sqlite_select_query, (id_user,))
        return int(cursor.fetchall()[0][0])
    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()


def add_clothe_to_clothes_list(id_look, id_clothe):
    try:
        sqlite_connection = sqlite3.connect('BeautyBotBase.db')
        cursor = sqlite_connection.cursor()
        sqlite_insert_query = """INSERT INTO ClothesList(IdLook,IdClothe) VALUES(?,?)"""
        cursor.execute(sqlite_insert_query, (id_look, id_clothe))
        sqlite_connection.commit()
        cursor.close()
    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()


def check_if_category_already_inserted(category, id_user):
    try:
        sqlite_connection = sqlite3.connect('BeautyBotBase.db')
        cursor = sqlite_connection.cursor()
        sqlite_select_query = """"""
        if category == "head":
            sqlite_select_query = """SELECT * FROM LookInputStatus  WHERE IdLookInputStatus= ? AND IsHeadCategotyInserted = 1"""
        elif category == "top":
            sqlite_select_query = """SELECT * FROM LookInputStatus  WHERE IdLookInputStatus= ? AND IsTopCategotyInserted = 1"""
        elif category == "bottom":
            sqlite_select_query = """SELECT * FROM LookInputStatus  WHERE IdLookInputStatus= ? AND IsBottomCategotyInserted = 1"""
        elif category == "footwear":
            sqlite_select_query = """SELECT * FROM LookInputStatus  WHERE IdLookInputStatus= ? AND IsFootwearCategoryInserted = 1"""
        elif category == "accesory":
            sqlite_select_query = """SELECT * FROM LookInputStatus  WHERE IdLookInputStatus= ? AND IsAccesoryCategoryInserted = 1"""
        cursor.execute(sqlite_select_query, (id_user,))
        if len(cursor.fetchall()) == 1:
            return True
        else:
            return False
    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()


def get_looks_list(id_user):
    try:
        sqlite_connection = sqlite3.connect('BeautyBotBase.db')
        cursor = sqlite_connection.cursor()
        sqlite_select_query = """SELECT * FROM Looks where IdUser = ?"""
        cursor.execute(sqlite_select_query, (id_user,))
        return cursor.fetchall()
    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()


def get_clothes_list(id_look):
    try:
        sqlite_connection = sqlite3.connect('BeautyBotBase.db')
        cursor = sqlite_connection.cursor()
        sqlite_select_query = """SELECT IdClothe FROM ClothesList where IdLook = ?"""
        cursor.execute(sqlite_select_query, (id_look,))
        return cursor.fetchall()
    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()

def clothe_by_id(id_clothe):
    try:
        sqlite_connection = sqlite3.connect('BeautyBotBase.db')
        cursor = sqlite_connection.cursor()
        sqlite_select_query = """SELECT * FROM Clothes where IdPhoto = ?"""
        cursor.execute(sqlite_select_query, (id_clothe,))
        return cursor.fetchall()
    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()
