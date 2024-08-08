import sender_stand_request
import data
def get_user_body(first_name):
    current_body = data.user_body.copy()
    current_body["firstName"] = first_name
    return current_body
def test_create_user_2_letter_in_first_name_get_success_response():
    user_body = get_user_body("Аа")
    user_response = sender_stand_request.post_new_user(user_body)
    assert user_response.status_code == 201
    assert user_response.json()["authToken"] != ""
    # В переменную users_table_response сохраняется результат запроса на получение данных из таблицы user_model
    users_table_response = sender_stand_request.get_users_table()
    # Строка, которая должна быть в ответе запроса на получение данных из таблицы users
    str_user = user_body["firstName"] + "," + user_body["phone"] + "," \
               + user_body["address"] + ",,," + user_response.json()["authToken"]

    # Проверка, что такой пользователь есть и он единственный
    assert users_table_response.text.count(str_user) == 1
# Функция для позитивной проверки
def positive_assert(first_name):
    # В переменную user_body сохраняется обновлённое тело запроса
    user_body = get_user_body(first_name)
    # В переменную user_response сохраняется результат запроса на создание пользователя:
    user_response = sender_stand_request.post_new_user(user_body)

    # Проверяется, что код ответа равен 201
    assert user_response.status_code == 201
    # Проверяется, что в ответе есть поле authToken и оно не пустое
    assert user_response.json()["authToken"] != ""

    # В переменную users_table_response сохраняется результат запроса на получение данных из таблицы user_model
    users_table_response = sender_stand_request.get_users_table()

    # Строка, которая должна быть в ответе
    str_user = user_body["firstName"] + "," + user_body["phone"] + "," \
               + user_body["address"] + ",,," + user_response.json()["authToken"]

    # Проверка, что такой пользователь есть и он единственный
    assert users_table_response.text.count(str_user) == 1

# Тест 1. Успешное создание пользователя
# Параметр fisrtName состоит из 2 символов
def test_create_user_2_letter_in_first_name_get_success_response():
    positive_assert("Aa")
# Тест 2. Успешное создание пользователя
# Параметр firstName состоит из 15 символов
def test_create_user_15_letter_in_first_name_get_success_response():
     positive_assert("Ааааааааааааааа")


def negative_assert_symbol(first_name):
    # В переменную user_body сохраняется обновлённое тело запроса
    user_body = get_user_body(first_name)

    # В переменную response сохраняется результат запроса
    response = sender_stand_request.post_new_user(user_body)

    # Проверка, что код ответа равен 400
    assert response.status_code == 400

    # Проверка, что в теле ответа атрибут "code" равен 400
    assert response.json()["code"] == 400
    # Проверка текста в теле ответа в атрибуте "message"
    assert response.json()["message"] == "Имя пользователя введено некорректно. " \
                                         "Имя может содержать только русские или латинские буквы, " \
                                         "длина должна быть не менее 2 и не более 15 символов"
# Тест 3. Ошибка
    # Параметр fisrtName состоит из 1 символа
def test_create_user_1_letter_in_first_name_get_error_response():
    negative_assert_symbol("A")

# Тест 4. Ошибка
# Параметр fisrtName состоит из 16 символов
def test_create_user_16_letter_in_first_name_get_error_response():
    negative_assert_symbol("Аааааааааааааааa")

# Тест 5. Успешное создание пользователя
    # Параметр fisrtName состоит из английских букв
def test_create_user_english_letter_in_first_name_get_success_response():
    positive_assert("QWErty")