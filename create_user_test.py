import sender_stand_request
import data


def get_user_body(first_name):
    current_body = data.user_body.copy()
    current_body["firstName"] = first_name
    return current_body


def positive_assert(first_name):
    user_body = get_user_body(first_name)
    user_response = sender_stand_request.post_new_user(user_body)

    assert user_response.status_code == 201
    assert user_response.json()["authToken"] != ""

    users_table_response = sender_stand_request.get_users_table()

    str_user = user_body["firstName"] + "," + user_body["phone"] + "," \
               + user_body["address"] + ",,," + user_response.json()["authToken"]

    assert users_table_response.text.count(str_user) == 1


def negative_assert_symbol(first_name):
    user_body = get_user_body(first_name)
    user_response = sender_stand_request.post_new_user(user_body)

    assert user_response.status_code == 400
    assert user_response.json()["code"] == 400

    message_response = "Имя пользователя введено некорректно. " \
                       "Имя может содержать только русские или латинские буквы, " \
                       "длина должна быть не менее 2 и не более 15 символов"

    assert user_response.json()["message"] == message_response


def negative_assert_no_first_name(user_body):
    user_response = sender_stand_request.post_new_user(user_body)
    assert user_response.status_code == 400
    assert user_response.json()["code"] == 400

    message_response = "Не все необходимые параметры были переданы"

    assert user_response.json()["message"] == message_response


def negative_assert_by_status_code(user_body):
    user_response = sender_stand_request.post_new_user(user_body)
    assert user_response.status_code == 400


# Тест 1. Успешное создание пользователя (имя - 2 символа)

def test_create_user_2_letter_in_first_name_get_success_response():
    positive_assert("Aa")


# Тест 2. Успешное создание пользователя (имя - 15 символов)
def test_create_user_15_letter_in_first_name_get_success_response():
    positive_assert("Aфффффффффффффa")


# Тест 4. Ошибочное создание пользователя (имя - более 15 символов)
def test_create_user_16_letter_in_first_name_get_success_response():
    negative_assert_symbol("AАфффффффффффффa")


# Тест 3. Ошибочное создание пользователя (имя -  менее 2 символов)
def test_create_user_1_letter_in_first_name_get_error_response():
    negative_assert_symbol("А")


# Тест 5. Успешное создание пользователя (анг. язык)
def test_create_user_english_letter_in_first_name_get_success_response():
    positive_assert("Lana")

# Тест 6. Успешное создание пользователя (русс. язык)
def test_create_user_russian_letter_in_first_name_get_success_response():
    positive_assert("Лана")


# Тест 7. Ошибочное создание пользователя (пробел)
def test_create_user_has_space_in_first_name_get_error_response():
    negative_assert_symbol("Ла на")


# Тест 8. Ошибочное создание пользователя (спецсимвол)
def test_create_user_has_special_symbol_in_first_name_get_error_response():
    negative_assert_symbol("Ла*на")


# Тест 9. Ошибочное создание пользователя (число)
def test_create_user_has_number_in_first_name_get_error_response():
    negative_assert_symbol("1Лана")


# Тест 10. Ошибочное создание пользователя (нет имени)
def test_create_user_no_first_name_get_error_response():
    user_body = data.user_body.copy()
    user_body.pop("firstName")
    negative_assert_no_first_name(user_body)


# Тест 11. Ошибочное создание пользователя (пустая строка)
def test_create_user_empty_first_name_get_error_response():
    user_body = get_user_body("")
    negative_assert_no_first_name(user_body)


# Тест 12. Ошибочное создание пользователя (только числа)
def test_create_user_number_type_first_name_get_error_response():
    user_body = get_user_body(12)
    negative_assert_by_status_code(user_body)