from api import PetFriends
from settings import valid_email, valid_password, invalid_password, invalid_email
import os

pf = PetFriends()


def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
#Ïîëó÷åíèå êëþ÷à ñ âàëèäíûìè äàííûìè. Áàçîâûé ïîëîæèòåëüíûé ñöåíàðèé

    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert 'key' in result


def test_get_api_key_for_invalid_user_psw(email=valid_email, password=invalid_password):
# Ïîëó÷åíèå êëþ÷à ñ íå âàëèäíûì ïàðîëåì. Íåãàòèâíûé ñöåíàðèé

    status, result = pf.get_api_key(email, password)
    print(result)
    assert status == 403


def test_get_api_key_for_invalid_user_email(email=invalid_email, password=valid_password):
# Ïîëó÷åíèå êëþ÷à ñ íå âàëèäíûì email. Íåãàòèâíûé ñöåíàðèé

    status, result = pf.get_api_key(email, password)
    assert status == 403


def test_get_all_pets_with_valid_key(filter=''):
#Ïîëó÷åíèå ñïèñêà ïèòîìöåâ ñ âàëèäíûì êëþ÷îì. Áàçîâûé ïîçèòèâíûé ñöåíàðèé.

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0


def test_add_new_pet_with_valid_data(name='Òóçèê', animal_type='Äâîðíÿãà', age='2', pet_photo='images/photo_dog.jpeg'):
# Äîáàâëåíèå ïèòîìöà ñ âàëèäíûìè äàííûìè. Áàçîâûé ïîçèòèâíûé ñöåíàðèé.

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 200
    assert result['name'] == name


def test_add_new_pet_with_invalid_photo_txt(name='Òóçèê', animal_type='Äâîðíÿãà', age='2', pet_photo='images/photo_dog_invalid.txt'):
# Äîáàâëåíèå ïèòîìöà ñ íå âàëèäíûì ôîòî. Íåãàòèâíûé ñöåíàðèé.

    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_add_new_pet(auth_key, name, animal_type, age, pet_photo)
    assert status == 400


def test_successful_delete_pet():
# Óäàëåíèå ïèòîìöà. Áàçîâûé ïîçèòèâíûé ñöåíàðèé.
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Ñóïåðäîã", "Äîã", "3", "images/photo_dog.jpeg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    assert status == 200
    assert pet_id not in my_pets.values()


def test_successful_delete_of_deleted_pet():
# Óäàëåíèå óæå óäàëåííîãî ïèòîìöà. Íåãàòèâíûé ñöåíàðèé
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Ñóïåðäîã", "Äîã", "3", "images/photo_dog.jpeg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)
    status, _ = pf.delete_pet(auth_key, pet_id)

    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    assert status == 200
    assert pet_id not in my_pets.values()


def test_successful_update_self_pet_info(name='Tuzik', animal_type='Æåâàñòèê', age=1):
#Îáíîâëåíèå äàííûõ. Ïîçèòèâíûé ñöåíàðèé.

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) > 0:
        status, result = pf.get_update_pet(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)
        assert status == 200
        assert result['name'] == name
    else:
        raise Exception("There is no my pets")


def test_add_new_pet_without_photo(name='Áàðñèê', animal_type='Òóçÿìáà', age='2'):
#Äîáàâëåíèå ïèòîìöà áåç ôîòî. Áàçîâûé ïîçèòèâíûé ñöåíàðèé.

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)
    assert status == 200
    assert result['name'] == name


def test_add_new_pet_with_long_name(animal_type='Òóçÿìáà', age='2'):
# Äîáàâëåíèå ïèòîìöà ñ äëèííûì èìåíåì. Áàçîâûé ïîçèòèâíûé ñöåíàðèé.

    name = """Òóçèê âûøåë ïîãóëÿòü è ïîéìàë ëÿãóøêó 
    âîáùåì Òóçèê ìîëîäåö íî íàôèã ìíå ëÿãóøêà
    ëó÷øå á Òóçèê ïðèòàùèë òîëñòóþ êóðèöó"""
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)
    assert status == 200
    assert result['name'] == name


def test_add_new_pet_with_special_characters_in_name(name='DoG_doG123!@#5647.,?#', animal_type='Òóçÿìáà', age='2'):
#Äîáàâëåíèå ïèòîìöà ñî ñïåöñèìâîëàìè â èìåíè. Ïîçèòèâíûé ñöåíàðèé.

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)
    assert status == 200
    assert result['name'] == name


def test_add_new_pet_with_only_numbers_in_name(name='12345678', animal_type='Òóçÿìáà', age='2'):
#Äîáàâëåíèå ïèòîìöà ñ öåëûìè ÷èñëàìè â èìåíè. Íåãàòèâíûé ñöåíàðèé.

    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)
    assert status == 400
    assert result['name'] != name


def test_add_new_pet_with_age_not_number(name='Áàðñèê', animal_type='Òóçÿìáà', age='twelve'):
#Äîáàâëåíèå ïèòîìöà ñ âîçðàñòîì íå ÷èñëîâûå çíà÷åíèÿ. Íåãàòèâíûé ñöåíàðèé.
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.add_new_pet_without_photo(auth_key, name, animal_type, age)
    assert status == 400
    assert result['age'] == age


def test_successful_add_photo_of_pet(pet_photo='images/photo_dog.jpeg'):
#Äîáàâëåíèå ôîòî. Ïîçèòèâíûé ñöåíàðèé.
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    if len(my_pets['pets']) > 0:
        status, result = pf.add_photo_of_pet(auth_key, my_pets['pets'][0]['id'], pet_photo)

        assert status == 200
        assert 'pet_photo' in result
    else:
        raise Exception("There is no my pets")
