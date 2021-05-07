import beauty_database_worker
import db_stateworker
import config
import os
import telebot
from telebot import types

bot = telebot.TeleBot(config.token)

dict_id_photo_id_user = {}
#db_stateworker.set_state(1019091731, config.States.S_START.value)

@bot.message_handler(commands=["start"],func=lambda message:
                     db_stateworker.get_current_state(message.from_user.id) == config.States.S_START.value)
def start_usage(message):
    if beauty_database_worker.is_user_registered(message.from_user.id) == False:
        try:

            os.mkdir("Users/{}".format(message.from_user.id))
            os.mkdir("Users/{}/Clothes".format(message.from_user.id))
            beauty_database_worker.add_user(message.from_user.id, message.from_user.first_name,
                                            message.from_user.last_name)
            db_stateworker.set_state(message.from_user.id, config.States.S_START.value)
            bot.send_message(message.chat.id, "Пользователь добавлен")
        except Exception as e:
            print(e)
            bot.send_message(message.chat.id, "Что-то пошло не так")
    else:
        bot.send_message(message.chat.id, "Вы уже зарегестрировались!")


@bot.message_handler(commands=["addclothes"],
                     func=lambda message:
                     db_stateworker.get_current_state(message.from_user.id) == config.States.S_START.value)
def add_clothes(message):
    db_stateworker.set_state(message.from_user.id, config.States.S_ADDCLOTHES_SEND_PIC.value)
    bot.send_message(message.chat.id, "Загрузите фотографию вещи")


@bot.message_handler(content_types=["photo"],
                     func=lambda message: db_stateworker.get_current_state(
                         message.from_user.id) == config.States.S_ADDCLOTHES_SEND_PIC.value)
def add_users_photo(message):
    try:
        file_info = bot.get_file(message.photo[len(message.photo) - 1].file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        src = 'Users/{}/Clothes/'.format(message.from_user.id) + str(file_info.file_path).split("/")[1]
        with open(src, 'wb') as new_file:
            new_file.write(downloaded_file)
        bot.reply_to(message, "Фото добавлено")
        beauty_database_worker.add_photo(message.from_user.id, src)
        id_photo = beauty_database_worker.get_last_created_photo_id(message.from_user.id)
        beauty_database_worker.add_empty_user_to_clothes_temp(message.from_user.id, id_photo)
        id_user = message.from_user.id
        db_stateworker.set_state(message.from_user.id, config.States.S_ADDCLOTHES_GET_DESK_GENDER_TYPE.value)
        dict_id_photo_id_user[id_user] = id_photo;
        inline_btn_man = types.InlineKeyboardButton('Мужской',
                                                    callback_data='button_choice_gender_man_{}_{}'.format(id_photo,
                                                                                                          id_user))
        inline_btn_woman = types.InlineKeyboardButton('Женский',
                                                      callback_data='button_choice_gender_woman_{}_{}'.format(id_photo,
                                                                                                              id_user))
        inline_btn_unisex = types.InlineKeyboardButton('Унисекс',
                                                       callback_data='button_choice_gender_unisex_{}_{}'.format(
                                                           id_photo, id_user))
        inline_kb_gender = types.InlineKeyboardMarkup().add(inline_btn_man, inline_btn_woman, inline_btn_unisex)
        bot.send_message(message.chat.id, "Теперь, пожалуйста, выберите пол", reply_markup=inline_kb_gender)
    except Exception as e:
        print(e)
        print("Что-то пошло не так")


@bot.callback_query_handler(func=lambda call: call.data.startswith('button_choice_gender') and
                                              db_stateworker.get_current_state(int(call.data.split("_")[
                                                                                       5])) == config.States.S_ADDCLOTHES_GET_DESK_GENDER_TYPE.value)
def process_callback_Kb_gender(call):
    sex = call.data.split("_")[3]
    id_photo = int(call.data.split("_")[4])
    user_id = int(call.data.split("_")[5])
    beauty_database_worker.update_clothes_temp_table_gender_type(id_photo, sex)
    db_stateworker.set_state(user_id, config.States.S_ADDCLOTHES_GET_DESK_SEASON_TYPE.value)
    inline_btn_summer = types.InlineKeyboardButton('Лето',
                                                   callback_data='button_choice_season_summer_{}_{}'.format(id_photo,
                                                                                                            user_id))
    inline_btn_winter = types.InlineKeyboardButton('Зима',
                                                   callback_data='button_choice_season_winter_{}_{}'.format(id_photo,
                                                                                                            user_id))
    inline_btn_spring = types.InlineKeyboardButton('Весна',
                                                   callback_data='button_choice_season_spring_{}_{}'.format(id_photo,
                                                                                                            user_id))
    inline_btn_autumn = types.InlineKeyboardButton('Осень',
                                                   callback_data='button_choice_season_autumn_{}_{}'.format(id_photo,
                                                                                                            user_id))
    inline_btn_demi = types.InlineKeyboardButton('Демисезон',
                                                 callback_data='button_choice_season_demiseason_{}_{}'.format(id_photo,
                                                                                                              user_id))
    inline_btn_noseason = types.InlineKeyboardButton('Без сезона',
                                                     callback_data='button_choice_season_noseason_{}_{}'.format(
                                                         id_photo, user_id))
    inline_kb_season = types.InlineKeyboardMarkup().add(inline_btn_summer, inline_btn_winter, inline_btn_spring,
                                                        inline_btn_autumn, inline_btn_demi, inline_btn_noseason)
    bot.send_message(call.message.chat.id, "Теперь давайте выберем сезон", reply_markup=inline_kb_season)


@bot.callback_query_handler(func=lambda call: call.data.startswith('button_choice_season') and
                                              db_stateworker.get_current_state(int(call.data.split("_")[
                                                                                       5])) == config.States.S_ADDCLOTHES_GET_DESK_SEASON_TYPE.value)
def process_callback_kb_season(call):
    season = call.data.split("_")[3]
    id_photo = int(call.data.split("_")[4])
    id_user = int(call.data.split("_")[5])
    beauty_database_worker.update_clothes_temp_table_season_type(id_photo, season)
    db_stateworker.set_state(id_user, config.States.S_ADDCLOTHES_GET_DESK_Category.value)
    inline_btn_head = types.InlineKeyboardButton("Голова",
                                                 callback_data='button_choice_category_head_{}_{}'.format(id_photo,
                                                                                                          id_user))
    inline_btn_top = types.InlineKeyboardButton("Верх",
                                                callback_data='button_choice_category_top_{}_{}'.format(id_photo,
                                                                                                        id_user))
    inline_btn_bottom = types.InlineKeyboardButton("Низ",
                                                   callback_data='button_choice_category_bottom_{}_{}'.format(id_photo,
                                                                                                              id_user))
    inline_btn_footwear = types.InlineKeyboardButton("Обувь",
                                                     callback_data='button_choice_category_footwear_{}_{}'.format(
                                                         id_photo,
                                                         id_user))
    inline_btn_accessory = types.InlineKeyboardButton("Акксесуар",
                                                      callback_data='button_choice_category_accessory_{}_{}'.format(
                                                          id_photo,
                                                          id_user))
    inline_kb_category = types.InlineKeyboardMarkup().add(inline_btn_head, inline_btn_top, inline_btn_bottom,
                                                          inline_btn_footwear, inline_btn_accessory)
    bot.send_message(call.message.chat.id, "Теперь выберите категорию", reply_markup=inline_kb_category)


@bot.callback_query_handler(func=lambda call: call.data.startswith('button_choice_category') and
                                              db_stateworker.get_current_state(int(call.data.split("_")[
                                                                                       5])) == config.States.S_ADDCLOTHES_GET_DESK_Category.value)
def process_callback_kb_category(call):
    category = call.data.split("_")[3]
    id_photo = int(call.data.split("_")[4])
    id_user = int(call.data.split("_")[5])
    beauty_database_worker.update_clothes_temp_table_category(id_photo, category)
    db_stateworker.set_state(id_user, config.States.S_ADDCLOTHES_GET_DESK_CategoryType.value)
    kb = get_category_kb_type_desc(category, 'button_choice_typecategory', id_user, id_photo)
    bot.send_message(call.message.chat.id, "Выберите тип вещи", reply_markup=kb)


def get_category_kb_type_desc(category, callback_start, id_user, id_photo=None):
    if category == "head":
        inline_btn_head_cap = types.InlineKeyboardButton("Кепка",
                                                         callback_data='{}_head_cap_{}_{}'.format(callback_start,
                                                             id_photo,
                                                             id_user))
        inline_btn_head_hat = types.InlineKeyboardButton("Шляпа",
                                                         callback_data='{}_head_hat_{}_{}'.format(callback_start,
                                                             id_photo,
                                                             id_user))
        inline_btn_head_hathead = types.InlineKeyboardButton("Шапка",
                                                             callback_data='{}_head_hathead_{}_{}'.format(callback_start,
                                                             id_photo,
                                                             id_user))
        inline_btn_head_headanother = types.InlineKeyboardButton("Другое",
                                                                 callback_data='{}_head_another_{}_{}'.format(callback_start,
                                                             id_photo,
                                                             id_user))
        inline_kb_category_head = types.InlineKeyboardMarkup().add(inline_btn_head_cap, inline_btn_head_hat,
                                                                   inline_btn_head_hathead, inline_btn_head_headanother)
        return inline_kb_category_head
    elif category == "top":
        inline_btn_top_TShirt = types.InlineKeyboardButton("Футболка",
                                                           callback_data='{}_top_TShirt_{}_{}'.format(callback_start,
                                                             id_photo,
                                                             id_user))
        inline_btn_top_blouse = types.InlineKeyboardButton("Блузка",
                                                           callback_data='{}_top_blouse_{}_{}'.format(callback_start,
                                                             id_photo,
                                                             id_user))
        inline_btn_top_shirt = types.InlineKeyboardButton("Рубашка",
                                                          callback_data='{}_top_shirt_{}_{}'.format(callback_start,
                                                             id_photo,
                                                             id_user))
        inline_btn_top_hoody = types.InlineKeyboardButton("Толстовка",
                                                          callback_data='{}_top_hoody_{}_{}'.format(callback_start,
                                                             id_photo,
                                                             id_user))
        inline_btn_top_top = types.InlineKeyboardButton("Топ",
                                                        callback_data='{}_top_top_{}_{}'.format(callback_start,
                                                             id_photo,
                                                             id_user))
        inline_btn_top_sweater = types.InlineKeyboardButton("Свитер",
                                                            callback_data='{}_top_sweater_{}_{}'.format(callback_start,
                                                             id_photo,
                                                             id_user))
        inline_btn_top_jumper = types.InlineKeyboardButton("Джемпер",
                                                           callback_data='{}_top_jumper_{}_{}'.format(callback_start,
                                                             id_photo,
                                                             id_user))
        inline_btn_top_another = types.InlineKeyboardButton("Другое",
                                                            callback_data='{}_top_another_{}_{}'.format(callback_start,
                                                             id_photo,
                                                             id_user))
        inline_kb_category_top = types.InlineKeyboardMarkup().add(inline_btn_top_TShirt, inline_btn_top_blouse,
                                                                  inline_btn_top_shirt, inline_btn_top_hoody,
                                                                  inline_btn_top_top, inline_btn_top_sweater,
                                                                  inline_btn_top_jumper, inline_btn_top_another)
        return inline_kb_category_top
    elif category == "bottom":
        inline_btn_bottom_jeans = types.InlineKeyboardButton("Джинсы",
                                                             callback_data='{}_bottom_jeens_{}_{}'.format(callback_start,
                                                             id_photo,
                                                             id_user))
        inline_btn_bottom_trousers = types.InlineKeyboardButton("Брюки",
                                                                callback_data='{}_bottom_trousers_{}_{}'.format(callback_start,
                                                             id_photo,
                                                             id_user))
        inline_btn_bottom_sweatpants = types.InlineKeyboardButton("Спортивные штаны",
                                                                  callback_data='{}_bottom_sweatpants_{}_{}'.format(callback_start,
                                                             id_photo,
                                                             id_user))
        inline_btn_bottom_leggins = types.InlineKeyboardButton("Леггинсы",
                                                               callback_data='{}_bottom_leggins_{}_{}'.format(callback_start,
                                                             id_photo,
                                                             id_user))
        inline_btn_bottom_another = types.InlineKeyboardButton("Другое",
                                                               callback_data='{}_bottom_another_{}_{}'.format(callback_start,
                                                             id_photo,
                                                             id_user))
        inline_kb_category_bottom = types.InlineKeyboardMarkup().add(inline_btn_bottom_jeans,
                                                                     inline_btn_bottom_trousers,
                                                                     inline_btn_bottom_sweatpants,
                                                                     inline_btn_bottom_leggins,
                                                                     inline_btn_bottom_another)
        return inline_kb_category_bottom
    elif category == "footwear":
        inline_btn_bottom_sneakers = types.InlineKeyboardButton("Кроссовки",
                                                                callback_data='{}_footwear_sneakers_{}_{}'.format(callback_start,
                                                             id_photo,
                                                             id_user))
        inline_btn_footwear_highshoes = types.InlineKeyboardButton("Туфли",
                                                                   callback_data='{}_footwear_shoes_{}_{}'.format(callback_start,
                                                             id_photo,
                                                             id_user))
        inline_btn_footwear_sandals = types.InlineKeyboardButton("Босоножки",
                                                                 callback_data='{}_footwear_sandals_{}_{}'.format(callback_start,
                                                             id_photo,
                                                             id_user))
        inline_btn_footwear_gumshoes = types.InlineKeyboardButton("Кеды",
                                                                  callback_data='{}_footwear_gumshoes_{}_{}'.format(callback_start,
                                                             id_photo,
                                                             id_user))
        inline_btn_footwear_boots = types.InlineKeyboardButton("Сапоги",
                                                               callback_data='{}_footwear_boots_{}_{}'.format(callback_start,
                                                             id_photo,
                                                             id_user))
        inline_btn_footwear_another = types.InlineKeyboardButton("Другое",
                                                                 callback_data='{}_footwear_another_{}_{}'.format(callback_start,
                                                             id_photo,
                                                             id_user))
        inline_kb_category_footwear = types.InlineKeyboardMarkup().add(inline_btn_bottom_sneakers,
                                                                       inline_btn_footwear_highshoes,
                                                                       inline_btn_footwear_sandals,
                                                                       inline_btn_footwear_gumshoes,
                                                                       inline_btn_footwear_boots,
                                                                       inline_btn_footwear_another)
        return inline_kb_category_footwear
    elif category == "accessory":
        inline_btn_accessory_clocks = types.InlineKeyboardButton("Часы",
                                                                 callback_data='{}_accessory_clocks_{}_{}'.format(callback_start,
                                                             id_photo,
                                                             id_user))
        inline_btn_accessory_glasses = types.InlineKeyboardButton("Очки",
                                                                  callback_data='{}_accessory_glasses_{}_{}'.format(callback_start,
                                                             id_photo,
                                                             id_user))
        inline_btn_accessory_bag = types.InlineKeyboardButton("Сумка",
                                                              callback_data='{}_accessory_bag_{}_{}'.format(callback_start,
                                                             id_photo,
                                                             id_user))
        inline_btn_accessory_scarf = types.InlineKeyboardButton("Шарф",
                                                                callback_data='{}_accessory_scarf_{}_{}'.format(callback_start,
                                                             id_photo,
                                                             id_user))
        inline_btn_accessory_backpack = types.InlineKeyboardButton("Рюкзак",
                                                                   callback_data='{}_accessory_backpack_{}_{}'.format(callback_start,
                                                             id_photo,
                                                             id_user))
        inline_btn_accessory_another = types.InlineKeyboardButton("Другое",
                                                                  callback_data='{}_accessory_another_{}_{}'.format(callback_start,
                                                             id_photo,
                                                             id_user))
        inline_kb_category_accessory = types.InlineKeyboardMarkup().add(inline_btn_accessory_clocks,
                                                                        inline_btn_accessory_glasses,
                                                                        inline_btn_accessory_bag,
                                                                        inline_btn_accessory_scarf,
                                                                        inline_btn_accessory_backpack,
                                                                        inline_btn_accessory_another)
        return inline_kb_category_accessory

@bot.callback_query_handler(func=lambda call: call.data.startswith('button_choice_typecategory') and
                                              db_stateworker.get_current_state(int(call.data.split("_")[
                                                                                       6])) == config.States.S_ADDCLOTHES_GET_DESK_CategoryType.value)
def process_callback_kb_category_type(call):
    category_type = call.data.split("_")[4]
    id_photo = int(call.data.split("_")[5])
    id_user = int(call.data.split("_")[6])
    beauty_database_worker.update_clothes_temp_table_category_type(id_photo, category_type)
    db_stateworker.set_state(id_user, config.States.S_ADDCLOTHES_GET_DESK_Color.value)
    bot.send_message(call.message.chat.id, "Теперь введите цвет")



@bot.message_handler(content_types=["text"],
                     func=lambda message: db_stateworker.get_current_state(
                         message.from_user.id) == config.States.S_ADDCLOTHES_GET_DESK_Color.value)
def get_color_text(message):
    beauty_database_worker.update_clothes_temp_table_color(dict_id_photo_id_user[message.from_user.id], message.text);
    bot.send_message(message.chat.id, "Цвет успешно добавлен")
    bot.send_message(message.chat.id, "Теперь добавьте название вещи")
    db_stateworker.set_state(message.from_user.id, config.States.S_ADDCLOTHES_GET_DESK_Name.value)


@bot.message_handler(content_types=["text"],
                     func=lambda message: db_stateworker.get_current_state(
                         message.from_user.id) == config.States.S_ADDCLOTHES_GET_DESK_Name.value)
def get_name_text(message):
    beauty_database_worker.update_clothes_temp_table_name(dict_id_photo_id_user[message.from_user.id], message.text)
    bot.send_message(message.chat.id, "Название успешно добавлено")
    db_stateworker.set_state(message.from_user.id, config.States.S_START.value)
    beauty_database_worker.transport_from_temp_clothes_to_clothes(dict_id_photo_id_user[message.from_user.id])
    beauty_database_worker.delete_clothes_from_clothes_temp(dict_id_photo_id_user[message.from_user.id])
    del dict_id_photo_id_user[message.from_user.id]
    bot.send_message(message.chat.id, "Описание вещи успешно закончено.")

@bot.message_handler(commands=["viewclothes"],
                    func=lambda message:
                   db_stateworker.get_current_state(message.from_user.id) == config.States.S_START.value)
def view_clothes(message):
    id_user = message.from_user.id
    inline_btn_select_view_type_all = types.InlineKeyboardButton("Просмотреть все",
                                                                 callback_data="inline_btn_select_view_type_all_{}".format(id_user))
    inline_btn_select_view_type_certain = types.InlineKeyboardButton("Выбрать тип вещи",
                                                                 callback_data="inline_btn_select_view_type_certain_{}".format(
                                                                     id_user))
    inline_kb_select_view_type = types.InlineKeyboardMarkup(row_width=1).add(inline_btn_select_view_type_all,
                                                                             inline_btn_select_view_type_certain)
    bot.send_message(message.chat.id, "Выберите что хотите просмотреть", reply_markup= inline_kb_select_view_type)
    db_stateworker.set_state(id_user, config.States.S_VIEWCLOTHES_View_Mode.value)


@bot.callback_query_handler(func=lambda message:
                   db_stateworker.get_current_state(message.from_user.id) == config.States.S_VIEWCLOTHES_View_Mode.value)
def process_view_type_handler(call):
    id_user = call.data.split("_")[6]
    view_mode = call.data.split("_")[5]
    if view_mode == "all":
        clothes_desc = beauty_database_worker.get_clothes(id_user)
        if len(clothes_desc) != 0:
            for desc in clothes_desc:
                description = "Пол: {}\nСезон: {}\nКатегория: {}\nТип: {}\nЦвет: {}\nОписание: {}".format(
                    config.gender_dictionary[desc[2]], config.season_dictionary[desc[3]],
                    config.category_dictionary[desc[4]],
                    config.category_type_dictionary[desc[5]], desc[6], desc[7])
                path = beauty_database_worker.get_photo_path(int(desc[1]))
                bot.send_photo(call.message.chat.id, photo=open(path, 'rb'), caption=description)
        else:
            bot.send_message(call.message.chat.id,"Нет вещей по данному запросу")
        db_stateworker.set_state(id_user, config.States.S_START.value)
    else:
        inline_btn_view_clothes_head = types.InlineKeyboardButton("Голова",
                                                      callback_data='b_c_v_clothes_head_{}'.format(id_user))
        inline_btn_view_clothes_top = types.InlineKeyboardButton("Верх",
                                                     callback_data='b_c_v_clothes_top_{}'.format(id_user))
        inline_btn_view_clothes_bottom = types.InlineKeyboardButton("Низ",
                                                        callback_data='b_c_v_clothes_bottom_{}'.format(id_user))
        inline_btn_view_clothes_footwear = types.InlineKeyboardButton("Обувь",
                                                          callback_data='b_c_v_clothes_footwear_{}'.format(id_user))
        inline_btn_view_clothes_accessory = types.InlineKeyboardButton("Акксесуар",
                                                           callback_data='b_c_v_clothes_accessory_{}'.format(id_user))
        inline_kb_view_clothes = types.InlineKeyboardMarkup().add(inline_btn_view_clothes_head,
                                                                  inline_btn_view_clothes_top,
                                                                  inline_btn_view_clothes_bottom,
                                                                  inline_btn_view_clothes_footwear,
                                                                  inline_btn_view_clothes_accessory)
        bot.send_message(id_user, "Выберите категорию", reply_markup=inline_kb_view_clothes)
        db_stateworker.set_state(id_user, config.States.S_VIEWCLOTHES_Category.value)


@bot.callback_query_handler(func=lambda call: call.data.startswith('b_c_v_clothes') and
                                              db_stateworker.get_current_state(int(call.data.split("_")[
                                                                                       5])) == config.States.S_VIEWCLOTHES_Category.value)
def select_category_to_view(call):
    id_user = call.data.split("_")[5]
    category = call.data.split("_")[4]
    kb = get_category_kb_type_desc(category, 'button_choice_view_categotyclothes', id_user)
    bot.send_message(call.message.chat.id, "Теперь выберете тип вещи",reply_markup= kb)
    db_stateworker.set_state(id_user, config.States.S_VIEWCLOTHES_Category_type.value)


@bot.callback_query_handler(func=lambda call: call.data.startswith('button_choice_view_categotyclothes') and
                                              db_stateworker.get_current_state(int(call.data.split("_")[
                                                                                       7])) == config.States.S_VIEWCLOTHES_Category_type.value)
def print_clothes_by_category_type(call):
    id_user = call.data.split("_")[7]
    category_type = call.data.split("_")[5]
    category = call.data.split("_")[4]
    clothes_desc = beauty_database_worker.get_clothes(id_user, category, category_type)
    print(clothes_desc)
    if len(clothes_desc) != 0:
        for desc in clothes_desc:
            description = "Пол: {}\nСезон: {}\nКатегория: {}\nТип: {}\nЦвет: {}\nОписание: {}".format(
                config.gender_dictionary[desc[2]], config.season_dictionary[desc[3]],
                config.category_dictionary[desc[4]],
                config.category_type_dictionary[desc[5]], desc[6], desc[7])
            path = beauty_database_worker.get_photo_path(int(desc[1]))
            bot.send_photo(call.message.chat.id, photo=open(path, 'rb'), caption=description)
    else:
        bot.send_message(call.message.chat.id, "Нет вещей по данному запросу")
    db_stateworker.set_state(id_user, config.States.S_START.value)



@bot.message_handler(commands=["addlook"],
                    func=lambda message:
                   db_stateworker.get_current_state(message.from_user.id) == config.States.S_START.value)
def set_look_on_conveyor(message):
    db_stateworker.set_state(message.from_user.id, config.States.S_IS_ADDLOOK_ON_PROCESS_Name.value)
    bot.send_message(message.from_user.id,"Введите название образа")


@bot.message_handler(content_types=["text"],
                     func=lambda message: db_stateworker.get_current_state(
                         message.from_user.id) == config.States.S_IS_ADDLOOK_ON_PROCESS_Name.value)
def get_name_text(message):
    name = message.text
    beauty_database_worker.create_emtpy_look(name, message.from_user.id)
    id_look = beauty_database_worker.get_last_created_look_id(message.from_user.id)
    beauty_database_worker.create_empty_look_insert_state_table(id_look)
    db_stateworker.set_state(message.from_user.id, config.States.S_ADDLOOK_CHECK_Category.value)
    add_look(message,message.from_user.id, id_look)


def add_look(message, user_id, id_look):
    db_stateworker.set_state(user_id, config.States.S_ADDLOOK_CHECK_Category_Types.value)
    arr_btn = []

    if not beauty_database_worker.check_if_category_already_inserted("head", id_look):
        inline_btn_look_head = types.InlineKeyboardButton("Голова",
                                                 callback_data='button_choice_look_head_{}_{}'.format(user_id, id_look))
        arr_btn.append(inline_btn_look_head)
    if not beauty_database_worker.check_if_category_already_inserted("top", id_look):
        inline_btn_look_top = types.InlineKeyboardButton("Верх",
                                                callback_data='button_choice_look_top_{}_{}'.format(user_id, id_look))
        arr_btn.append(inline_btn_look_top)
    if not beauty_database_worker.check_if_category_already_inserted("bottom", id_look):
        inline_btn_look_bottom = types.InlineKeyboardButton("Низ",
                                                   callback_data='button_choice_look_bottom_{}_{}'.format(user_id, id_look))
        arr_btn.append(inline_btn_look_bottom)
    if not beauty_database_worker.check_if_category_already_inserted("footwear", id_look):
        inline_btn_look_footwear = types.InlineKeyboardButton("Обувь",
                                                     callback_data='button_choice_look_footwear_{}_{}'.format(user_id, id_look))
        arr_btn.append(inline_btn_look_footwear)
    if not beauty_database_worker.check_if_category_already_inserted("accesory", id_look):
        inline_btn_look_accessory = types.InlineKeyboardButton("Акксесуар",
                                                  callback_data='button_choice_look_accessory_{}_{}'.format(user_id, id_look))
        arr_btn.append(inline_btn_look_accessory)
    inline_kb_look = types.InlineKeyboardMarkup()
    for btn in arr_btn:
        inline_kb_look.add(btn)
    bot.send_message(message.chat.id, "Выберите категорию", reply_markup=inline_kb_look)


@bot.callback_query_handler(func=lambda call: call.data.startswith('button_choice_look') and
                                              db_stateworker.get_current_state(int(call.data.split("_")[
                                                                                       4])) == config.States.S_ADDLOOK_CHECK_Category_Types.value)
def process_callback_category_type(call):
    category = call.data.split("_")[3]
    id_user = int(call.data.split("_")[4])
    id_look = int(call.data.split("_")[5])
    db_stateworker.set_state(id_user, config.States.S_IS_ADDLOOK_ON_PROCESS_Print_Categories.value)
    kb = get_category_kb_type_desc(category, 'button_choice_typelook_{}'.format(id_look), id_user)
    bot.send_message(call.message.chat.id, "Теперь выберите тип", reply_markup=kb)


@bot.callback_query_handler(func=lambda call: call.data.startswith('button_choice_typelook') and
                                              db_stateworker.get_current_state(int(call.data.split("_")[
                                                                                       7])) == config.States.S_IS_ADDLOOK_ON_PROCESS_Print_Categories.value)
def process_callback_kb_look_category_type(call):
    id_look = int(call.data.split("_")[3])
    category = call.data.split("_")[4]
    category_type = call.data.split("_")[5]
    id_user = int(call.data.split("_")[7])
    clothes_desc = beauty_database_worker.get_clothes(id_user, category, category_type)
    db_stateworker.set_state(id_user, config.States.S_IS_ADDLOOK_ON_PROCESS_Add_Clothe.value)
    print(clothes_desc)
    if len(clothes_desc) != 0:
        for desc in clothes_desc:
            description = "Пол: {}\nСезон: {}\nКатегория: {}\nТип: {}\nЦвет: {}\nОписание: {}".format(
                config.gender_dictionary[desc[2]], config.season_dictionary[desc[3]],
                config.category_dictionary[desc[4]],
                config.category_type_dictionary[desc[5]], desc[6], desc[7])
            path = beauty_database_worker.get_photo_path(int(desc[1]))
            inline_btn_look_add_clothes = types.InlineKeyboardButton(text="Выбрать",
                                                                  callback_data='button_look_add_clothes_{}_{}_{}'.format(
                                                                      desc[1],id_look,category))
            kb = types.InlineKeyboardMarkup().add(inline_btn_look_add_clothes)
            bot.send_photo(call.message.chat.id,photo=open(path, 'rb'), caption=description, reply_markup=kb)
    else:
        db_stateworker.set_state(id_user, config.States.S_ADDLOOK_WRONG.value)
        inline_btn_look_return = types.InlineKeyboardButton("Выйти в главное меню",
                                                                 callback_data='button_look_add_wrong_return_{}'.format(id_look))
        inline_btn_look_continue = types.InlineKeyboardButton("Вернуться к выбору",
                                                            callback_data='button_look_add_wrong_continue_{}'.format(id_look))
        kb = types.InlineKeyboardMarkup(row_width=1).add(inline_btn_look_return, inline_btn_look_continue)
        
        bot.send_message(call.message.chat.id, "Нет вещей в указанной категории", reply_markup= kb)
                                                                 
        
@bot.callback_query_handler(func=lambda call: call.data.startswith('button_look_add_wrong') and
                                              db_stateworker.get_current_state(int(call.from_user.id)
                                                                               == config.States.S_ADDLOOK_WRONG.value))
def wrong_choice(call):
    id_look = call.data.split("_")[5]
    choice = call.data.split("_")[4]
    if choice == "return":
        db_stateworker.set_state(call.from_user.id, config.States.S_START.value)
        beauty_database_worker.delete_look_input_status(id_look)
        beauty_database_worker.delete_look(id_look)
        bot.send_message(call.message.chat.id, "Вы успешно вышли в главное меню!")
    else:
        add_look(call.message, call.from_user.id, id_look)


@bot.callback_query_handler(func=lambda call: call.data.startswith('button_look_add_clothes') and
                                              db_stateworker.get_current_state(int(call.from_user.id)
                                                                               == config.States.S_IS_ADDLOOK_ON_PROCESS_Add_Clothe.value))
def add_clothes(call):
    id_clothe = call.data.split("_")[4]
    id_look = call.data.split("_")[5]
    category = call.data.split("_")[6]
    beauty_database_worker.set_look_state(id_look, category)
    id_user = call.from_user.id
    beauty_database_worker.add_clothe_to_clothes_list(id_look, id_clothe)
    if beauty_database_worker.is_look_inserted(id_look):
        db_stateworker.set_state(call.from_user.id, config.States.S_START.value)
        bot.send_message(call.message.chat.id,"Создание образа успешно закончено!")
        beauty_database_worker.delete_look_input_status(id_look)
        return
    add_look(call.message, id_user, id_look)

@bot.message_handler(commands=["viewlooks"],
                    func=lambda message:
                   db_stateworker.get_current_state(message.from_user.id) == config.States.S_START.value)
def view_look(message):
    id_user = message.from_user.id
    looks_list = beauty_database_worker.get_looks_list(id_user)
    if len(looks_list) == 0:
        bot.send_message(message.chat.id, "Нет добавленных образов")
        return
    kb = types.InlineKeyboardMarkup()
    for look in looks_list:
        btn = types.InlineKeyboardButton(text=str(look[2]), callback_data = "view_look_{}".format(look[0]))
        kb.add(btn)
    bot.send_message(message.chat.id, text="Выберите образ", reply_markup= kb)
    db_stateworker.set_state(message.from_user.id, config.States.S_VIEW_LOOK.value)


@bot.callback_query_handler(func=lambda call: call.data.startswith('view_look') and
                                              db_stateworker.get_current_state(call.from_user.id) == config.States.S_VIEW_LOOK.value)
def callback_view_look(call):
    id_look = call.data.split("_")[2]
    clothes_id = beauty_database_worker.get_clothes_list(id_look)

    for id_clothe in clothes_id:
        desc = beauty_database_worker.clothe_by_id(id_clothe[0])[0]
        description = "Пол: {}\nСезон: {}\nКатегория: {}\nТип: {}\nЦвет: {}\nОписание: {}".format(
            config.gender_dictionary[desc[2]], config.season_dictionary[desc[3]],
            config.category_dictionary[desc[4]],
            config.category_type_dictionary[desc[5]], desc[6], desc[7])
        path = beauty_database_worker.get_photo_path(int(desc[1]))
        bot.send_photo(call.message.chat.id, photo=open(path, 'rb'), caption=description)

    db_stateworker.set_state(call.from_user.id, config.States.S_START.value)

@bot.message_handler(commands=["deletelook"],
                    func=lambda message:
                   db_stateworker.get_current_state(message.from_user.id) == config.States.S_START.value)
def delete_look(message):
    id_user = message.from_user.id
    looks_list = beauty_database_worker.get_looks_list(id_user)
    if len(looks_list) == 0:
        bot.send_message(message.chat.id, "Нет добавленных образов")
        return
    kb = types.InlineKeyboardMarkup()
    for look in looks_list:
        btn = types.InlineKeyboardButton(text=str(look[2]), callback_data = "delete_look_{}".format(look[0]))
        kb.add(btn)
    bot.send_message(message.chat.id, text="Выберите образ", reply_markup= kb)
    db_stateworker.set_state(message.from_user.id, config.States.S_DELETE_LOOK.value)


@bot.callback_query_handler(func=lambda call: call.data.startswith('delete_look') and
                                              db_stateworker.get_current_state(call.from_user.id) == config.States.S_DELETE_LOOK.value)
def callback_view_clothes_to_delete(call):
    id_look = call.data.split("_")[2]
    beauty_database_worker.delete_look(id_look)
    bot.send_message(call.message.chat.id, "Образ успешно удален!")
    db_stateworker.set_state(call.from_user.id, config.States.S_START.value)




bot.infinity_polling()
