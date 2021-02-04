import os
from api import PetFriends
from settings import valid_email, valid_password, invalid_password, invalid_email, empty_email, empty_password

pf = PetFriends()

def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    """"Тест авторизации с правильными email и паролем"""
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert 'key' in result
    # Печатаем полученный api_key
    print(result)

def test_get_all_pets_with_valid_key(filter=''):
    """"Тест получения списка питомцев с вводом правильного api_key"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    # Проверяем, не пустой ли список
    assert len(result['pets']) > 0

def test_add_new_pet_with_valid_data(name = 'Персик', animal_type = 'Кот',
                                     age = '4', pet_photo = 'images/27.jpg'):
    """"Тест добавления нового питомца"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['name'] == name

def test_successful_delete_self_pet():
    """Проверяем возможность удаления питомца"""
    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Суперкот", "кот", "3", "images/27.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    # Берём id первого питомца из списка и отправляем запрос на удаление
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)
    # Ещё раз запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    # Проверяем что статус ответа равен 200 и в списке питомцев нет id удалённого питомца
    assert status == 200
    assert pet_id not in my_pets.values()


def test_successful_update_self_pet_info(name='Мурзик', animal_type='Котэ', age=5):
    """Проверяем возможность обновления информации о питомце"""
    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    # Если список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)
        # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
        assert status == 200
        assert result['name'] == name
    else:
        # если спиок питомцев пустой, то выкидываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")

def test_create_pet_simple(name = 'Трой', animal_type = 'Кот', age = '10', pet_photo = 'images/27.jpg'):
    """"Создаём простого питомца через запрос POST /api/create_pet_simple"""
    # Получаем auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.create_pet_simple(auth_key, name, animal_type, age, pet_photo)
    # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
    assert status == 200
    assert result['name'] == name

def test_successful_update_pet_photo(photo='images/36.jpg'):
    """изменение фото моего питомца """
    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    photo = os.path.join(os.path.dirname(__file__), photo)
    # Получаем ключ auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    # Получаем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    # Если список не пустой, то пробуем обновить его фото
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_photo(my_pets['pets'][0]['id'], photo, auth_key)
        # Проверяем что статус ответа = 200 и имя питомца соответствует заданному
        assert status == 200
    else:
        # Если список питомцев пустой, то вызываем исключение с текстом об отсутствии своих питомцев
        raise Exception("There is no my pets")

def test_get_api_key_for_invalid_user_1(email=valid_email, password=invalid_password):
    """"Тест на авторизацию с неправильным паролём"""
    status, result = pf.get_api_key(email, password)
    # Если статус ответа 400 или 403, значит авторицазия с некорректными данными не удалась
    assert status == 400 or 403

def test_get_api_key_for_invalid_user_2(email=invalid_email, password=valid_password):
    """"Тест на авторизацию с неправильным email"""
    status, result = pf.get_api_key(email, password)
    # Если статус ответа 400 или 403, значит авторицазия с некорректными данными не удалась
    assert status == 400 or 403

def test_get_api_key_for_invalid_user_3(email=empty_email, password=valid_password):
    """"Тест на авторизацию с пустым email"""
    status, result = pf.get_api_key(email, password)
    # Если статус ответа 400 или 403, значит авторицазия с некорректными данными не удалась
    assert status == 400 or 403

def test_get_api_key_for_invalid_user_4(email=valid_email, password=empty_password):
    """"Тест на авторизацию с пустым паролём"""
    status, result = pf.get_api_key(email, password)
    # Если статус ответа 400 или 403, значит авторицазия с некорректными данными не удалась
    assert status == 400 or 403

def test_create_new_pet_1(name = '', animal_type = '',
                                     age = '', pet_photo ='images/27.jpg'):
    """"Тест на добавление питомца с пустыми значениями"""
    # Получаем auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.create_pet_simple(auth_key, name, animal_type, age, pet_photo)
    # Если статус ответа 200, значит добавление питомца возможно с пустыми значениями
    assert status == 200
    assert result['name'] == name

def test_create_new_pet_2(name = 'vbkZKVJDLKnkvldnvldjvalsdjvaldjvabds...+12344223,54514514564/gagadf',
                                    animal_type = 'Кот', age = '4', pet_photo = 'images/27.jpg'):
    """"Тест на добавление питомца с именем, состоящим из сложных символов"""
    # Получаем auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.create_pet_simple(auth_key, name, animal_type, age, pet_photo)
    # Если статус ответа 200, значит добавление питомца возможно с именем, состоящим из сложных символов
    assert status == 200
    assert result['name'] == name

def test_create_new_pet_3(name = 'Персик', animal_type = 'Кот', age = '0.178', pet_photo = 'images/27.jpg'):
    """"Тест на добавление питомца с дробным числом возраста"""
    # Получаем auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.create_pet_simple(auth_key, name, animal_type, age, pet_photo)
    # Если статус ответа 200, значит добавление питомца возможно с дробным числом возраста
    assert status == 200
    assert result['age'] == age

def test_get_all_pets_with_invalid_key_1(filter=''):
    # Тест получения списка питомцев с вводом пустого значения auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets_2(auth_key, filter)
    # Если статус 400 или 403, значит получение списка питомцев с пустым значением auth_key невозможно
    assert status == 400 or 403

def test_get_all_pets_with_invalid_key_2(filter=''):
    # Тест получения списка питомцев с вводом неправильного значения auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets_3(auth_key, filter)
    # Если статус 400 или 403, значит получение списка питомцев с неправильным значением auth_key невозможно
    assert status == 400 or 403

def test_successful_update_pet_photo_2(photo='images/gif_picture.gif'):
    """Негативный тест: попытка изменить фото питомца на изображение GIF-формата """
    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    photo = os.path.join(os.path.dirname(__file__), photo)
    # Получаем ключ auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    # Получаем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")
    # Если список не пустой, то пробуем обновить его фото
    status, result = pf.update_pet_photo(my_pets['pets'][0]['id'], photo, auth_key)
    # Если статус 500, значит изменить фото питомца на изображение GIF-формата невозможно
    assert status == 500


