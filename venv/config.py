from enum import Enum

token = '1710310535:AAFeIh-QRvhcd3LN-1GIAllzulLsh-wqoTo'
db_state_file = "database_state.vdb"

gender_dictionary = {
    'man': "Мужской",
    'woman': 'Женский',
    'unisex': 'Унисекс'
}
season_dictionary = {
    'summer': 'Лето',
    'winter': 'Зима',
    'autumn': 'Осень',
    'spring': 'Весна',
    'demiseason': 'Демисезон',
    'noseason': 'Нет сезона'
}
category_dictionary = {
    'head': 'Голова',
    'top': 'Верх',
    'bottom': 'Низ',
    'footwear': 'Ноги',
    'accessory': 'Акксесуар'
}

category_type_dictionary = {
    'cap': 'Кепка',
    'hat': 'Шляпа',
    'hathead': 'Шапка',
    'another': 'Другое',
    'TShirt': 'Футболка',
    'blouse': 'Блузка',
    'shirt': 'Рубашка',
    'hoody': 'Толстовка',
    'top': 'Топ',
    'sweater': 'Свитер',
    'jumper': 'Джемпер',
    'jeens': 'Джинсы',
    'trousers': 'Брюки',
    'sweatpants': 'Спортивные штаны',
    'leggins': 'Леггинсы',
    'sneakers': 'Кроссовки',
    'shoes': 'Туфли',
    'sandals': 'Босоножки',
    'gumshoes': 'Кеды',
    'boots': 'Сапоги',
    'clocks': 'Часы',
    'glasses': 'Очки',
    'bag': 'Сумка',
    'scarf': 'Шарф',
    'backpack': 'Рюкзак'


}


class States(Enum):

    S_START = "0"
    S_ADDCLOTHES_SEND_PIC = "1"
    S_ADDCLOTHES_GET_DESK_GENDER_TYPE = "2"
    S_ADDCLOTHES_GET_DESK_SEASON_TYPE = "3"
    S_ADDCLOTHES_GET_DESK_Category = "4"
    S_ADDCLOTHES_GET_DESK_CategoryType = "5"
    S_ADDCLOTHES_GET_DESK_Color = "6"
    S_ADDCLOTHES_GET_DESK_Name = "7"
    S_VIEWCLOTHES_View_Mode = "8"
    S_VIEWCLOTHES_Category = "9"
    S_VIEWCLOTHES_Category_type = "10"
    S_ADDLOOK_CHECK_Category = "11"
    S_ADDLOOK_CHECK_Category_Types = "12"
    S_IS_ADDLOOK_ON_PROCESS_Name = "13"
    S_IS_ADDLOOK_ON_PROCESS_Print_Categories = "14"
    S_IS_ADDLOOK_ON_PROCESS_Add_Clothe = "15"
    S_ADDLOOK_WRONG = "16"
    S_VIEW_LOOK = "17"
    S_DELETE_LOOK_VIEW = "18"
    S_DELETE_LOOK = "19"


