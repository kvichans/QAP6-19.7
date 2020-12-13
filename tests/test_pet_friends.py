import os
from api import PetFriends
from settings import (valid_email, 
                      valid_password, 
                      not_valid_email, 
                      not_valid_password)


pf = PetFriends()


def test_get_api_key_for_valid_user(
    email=valid_email, 
    password=valid_password
):
    """ Проверяем, что запрос api ключа возвращает статус 200 и 
        в результате содержится слово key"""
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert 'key' in result


def test_get_api_key_for_not_valid_email_and_password(
    email=not_valid_email,
    password=not_valid_password
):
    """ Проверяем, что запрос api ключа с неверным email пользователя 
        возвращает статус 403 и в результате не содержится слово key"""
    status, result = pf.get_api_key(email, password)
    assert status == 403
    assert 'key' not in result


def test_get_all_pets_with_valid_key(filter=''):
    """ Проверяем, что запрос списка всех питомцев возвращает не пустой список.
        Для этого сначала получаем api ключ и сохраняем в переменную auth_key. 
        Далее, используя этот ключ, запрашиваем список всех питомцев и 
        проверяем, что список не пустой.
        Доступное значение параметра filter - pf.MY_PETS, pf.ALL_PETS """
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0


def test_add_new_pet_with_valid_data(
    name='Содерберг', 
    animal_type='Кот Египетский',
    age='3', 
    pet_photo_path='images/cat1.jpg'
):
    """ Проверяем, что запрос на добавление нового питомца 
        с указанными параметрами выполняется успешно."""
    pet_photo_path = os.path.join(os.path.dirname(__file__), pet_photo_path)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(
        auth_key, 
        name, 
        animal_type, 
        age, 
        pet_photo_path
    )

    assert status == 200
    assert result['name'] == name
    assert result['animal_type'] == animal_type


def test_add_new_pet_with_empty_age(
    name='Содерберг', 
    animal_type='Кот Египетский',
    age='', 
    pet_photo_path='images/cat1.jpg'
):
    """ Проверяем, что запрос на добавление нового питомца 
        с пустым полем возраста выполняется успешно"""
    pet_photo_path = os.path.join(os.path.dirname(__file__), pet_photo_path)

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(
        auth_key, 
        name, 
        animal_type, 
        age, 
        pet_photo_path
    )

    assert status == 200
    assert 'name' in result


def test_add_new_pet_with_negative_age(
    name='Содерберг', 
    animal_type='Кот Египетский',
    age='-7', 
    pet_photo_path='images/cat1.jpg'
):
    """ Проверяем, что запрос на добавление нового питомца 
        с отрицательным возрастом выполняется успешно"""
    pet_photo_path = os.path.join(os.path.dirname(__file__), pet_photo_path)

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(
        auth_key, 
        name, 
        animal_type, 
        age, 
        pet_photo_path
    )

    assert status == 200
    assert 'name' in result


def test_add_new_pet_with_space_in_age(
    name='Содерберг', 
    animal_type='Кот Египетский',
    age=' ', 
    pet_photo_path='images/cat1.jpg'
):
    """ Проверяем, что запрос на добавление нового питомца 
        с пустым полем возраста выполняется успешно"""
    pet_photo_path = os.path.join(os.path.dirname(__file__), pet_photo_path)

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo_path)

    assert status == 200
    assert 'name' in result


def test_add_new_pet_with_incorrect_age(
    name='Содберг', 
    animal_type='Кот Египетскай',
    age='333333333333333333333', 
    pet_photo_path='images/cat1.jpg'
):
    """ Проверяем, что запрос на добавление нового питомца 
        с некорректным параметром 
            возраст питомца = 333333333333333333333
        выполняется успешно."""
    pet_photo_path = os.path.join(os.path.dirname(__file__), pet_photo_path)

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(
        auth_key, 
        name, 
        animal_type, 
        age, 
        pet_photo_path
    )

    assert status == 200
    assert result['name'] == name
    assert result['age'] == age


def test_successful_delete_self_pet():
    """Проверяем возможность удаления питомца"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, pf.MY_PETS)

    # Проверяем, если список своих питомцев пустой, то добавляем нового питомца, 
    # и опять запрашиваем список своих питомцев
    if not my_pets['pets']:
        pf.add_new_pet(auth_key, "Котярыч", "Котяра", "2", "images/cat1.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, pf.MY_PETS)

    # Берём id первого питомца из списка и отправляем запрос на удаление
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    # Ещё раз запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, pf.MY_PETS)

    # Проверяем что статус ответа равен 200 и 
    # в списке питомцев нет id удалённого питомца
    assert status == 200
    assert pet_id not in [pet['id'] for pet in my_pets['pets']]


def test_successful_update_self_pet_info(
    name='Минималист', 
    animal_type='Котторт', 
    age=2
):
    """ Проверяем возможность обновления информации о питомце"""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, pf.MY_PETS)
    if not my_pets['pets']:
        raise Exception("There is no my pets")
    pet_id = my_pets['pets'][0]['id']

    status, result = pf.update_pet_info(auth_key, 
                                        pet_id, 
                                        name, 
                                        animal_type, 
                                        age)

    # Проверяем что статус ответа = 200 и атрибуты питомца поменялись
    assert status == 200
    assert result['name'] == name
    assert result['animal_type'] == animal_type
    assert result['age'] == str(age)


def test_rejection_update_self_pet_info_without_name(
    name='', 
    animal_type='преампуль', 
    age=2
):
    """ Проверяем невозможность очистить имя питомца 
        путём передачи пустого поля name """

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, pf.MY_PETS)
    if not my_pets['pets']:
        raise Exception("There is no my pets")
    pet_id = my_pets['pets'][0]['id']

    status, result = pf.update_pet_info(
        auth_key, 
        pet_id, 
        name, 
        animal_type, 
        age
    )

    # Проверяем что статус ответа = 200 и имя питомца не стало пустым
    assert status == 200
    assert result['name']


def test_rejection_update_self_pet_info_without_animal_type(
    name='Уася', 
    animal_type='', 
    age=1
):
    """ Проверяем невозможность очистить типа питомца путём 
        передачи пустого поля animal_type """

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, pf.MY_PETS)

    if not my_pets['pets']:
        raise Exception("There is no my pets")
    pet_id = my_pets['pets'][0]['id']

    status, result = pf.update_pet_info(
        auth_key, 
        pet_id, 
        name, 
        animal_type, 
        age
    )
    # Проверяем что статус ответа = 200 и тип питомца не пустой
    assert status == 200
    assert result['animal_type']


def test_succsessful_update_self_pet_info_with_spase_name(
    name=' ', 
    animal_type='прекурсор собакена',
    age=1
):
    """ Проверяем возможность очистки имени питомца путём передачи пробела
        в поле name - информация перезаписывается успешно."""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, pf.MY_PETS)

    if not my_pets['pets']:
        raise Exception("There is no my pets")
    pet_id = my_pets['pets'][0]['id']

    status, result = pf.update_pet_info(
        auth_key, 
        pet_id, 
        name, 
        animal_type, 
        age
    )
    # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
    assert status == 200
    assert result['name'] == ' '


def test_add_new_pet_with_valid_data_without_foto(
    name='Тростиночка',
    animal_type='Котетский', 
    age='1'):
    """ Проверяем, что запрос на добавление нового питомца 
        без фото с указанными параметрами выполняется успешно."""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_without_photo(
        auth_key, 
        name, 
        animal_type, 
        age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name


def test_add_new_pet_with_incorrect_data_without_foto(
    name='@#$%^&!*',
    animal_type='', 
    age=''
):
    """ Проверяем, что запрос на добавление нового питомца 
        без фото с некорректно указанными параметрами 
            name задаётся спецсимволами, 
            animal_type и age - пустые
        выполняется успешно."""

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_without_photo(
        auth_key, 
        name, 
        animal_type, 
        age
    )

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name


def test_successful_add_foto_of_pet(
    pet_id='', 
    pet_photo_path='images/cat1.jpg'):
    """Проверяем успешность запроса на добавление фото питомца по его id"""
    pet_photo_path = os.path.join(os.path.dirname(__file__), pet_photo_path)

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, pf.MY_PETS)
    if not my_pets['pets']:
        raise Exception("There is no my pets")
    pet_id = my_pets['pets'][0]['id']

    status, result = pf.add_foto_of_pet(auth_key, pet_id, pet_photo_path)

    # Проверяем что статус ответа = 200 и фото питомца соответствует заданному
    assert status == 200
    assert result['pet_photo']
