from geopy.geocoders import Nominatim
import re
# Функция для получения координат по адресу с сайта OpenStreetMap
def get_location(address):
    geolocator = Nominatim(user_agent='MyGeaopyUA')
    try:
        location = geolocator.geocode(address)
    except Exception as e:
        print(e)
        location = None
    if location:
        if location.raw.get('class') == 'building':
            return location.latitude, location.longitude
        else:
            print('It is not a building')
            return None
    else:
        print('location is empty on NominAPI')
        return None


def check_address_correct(address, house_number):
    house_number = re.sub(r'[\\]', '', house_number)
    cleaned_house_number = re.sub(r'[\\/]', '', house_number)
    if house_number == address.split()[-1] or cleaned_house_number == address.split()[-1]:
        return True
    else:
        return False


def clean_address(address):
    shortcuts = ['дом', 'респ', 'край', 'обл', 'гфз', 'аобл', 'аокр', 'мр-н', 'го', 'гп', 'сп', 'внр-н', 'внтерг',
                 'пос', 'р-н', 'с/с', 'г', 'пгт', 'рп', 'кп', 'гп', 'п', 'аал', 'арбан', 'аул',
                 'в-ки', 'г-к', 'з-ка', 'п-к', 'киш', 'п_ст', 'п_ж/д_ст', 'ж/д_бл-ст', 'ж/д_б-ка', 'ж/д_в-ка',
                 'ж/д_к-ма', 'ж/д_к-т', 'ж/д_пл-ма', 'ж/д_пл-ка', 'ж/д_пп', 'ж/д_оп',
                 'ж/д_рзд', 'ж/д_ст', 'м-ко', 'д', 'с', 'сл', 'ст-ца', 'ст', 'у', 'х', 'рзд', 'зим', 'б-г', 'вал',
                 'ж/р', 'зона', 'кв-л', 'мкр', 'ост-в', 'парк', 'платф', 'п/р', 'р-н',
                 'сад', 'сквер', 'тер', 'тер.', 'тер_СНО', 'тер_ОНО', 'тер_ДНО', 'тер_СНТ', 'тер_ОНТ', 'тер_ДНТ',
                 'тер_СПК', 'тер_ОПК', 'тер_ДПК', 'тер_СНП', 'тер_ОНП', 'тер_ДНП', 'тер_ТСН',
                 'тер_ГСК', 'ус', 'терфх', 'ю', 'ал', 'б-р', 'взв', 'взд', 'дор', 'ззд', 'км', 'к-цо', 'коса', 'лн',
                 'мгстр', 'наб', 'пер-д', 'пер', 'пл-ка', 'пл', 'пр-д', 'пр-к',
                 'пр-ка', 'пр-лок', 'пр-кт', 'проул', 'рзд', 'ряд', 'с-р', 'с-к', 'сзд', 'тракт', 'туп', 'ш', 'влд',
                 'г-ж', 'д', 'двлд', 'зд', 'з/у', 'кв', 'ком', 'подв', 'кот',
                 'п-б', 'к', 'ОНС', 'офис', 'пав', 'помещ', 'рабуч', 'скл', 'coop', 'стр', 'торгзал', 'цех'
                 ]

    # Объединяем сокращения в одно регулярное выражение
    shortcuts_regex = r'\b(?:' + '|'.join(map(re.escape, shortcuts)) + r')\b'

    # Удаляем сокращения из адреса
    address = re.sub(shortcuts_regex, '', address)

    return address

# Изменяем адрес для поиска: К примеру в базе адрес :СНТ Строитель 2 n3, 64" - для Яндекса нужно сделать "СНТ Строитель-3, 64"
def modify_address_for_Yandex(address):
    if 'сад' in address:
        address = address.replace('сад', '')

    address = address.replace('  ', ' ')

    address = re.sub(r'(?<=\d) n | n(?=\d)', '-', address)
    address = re.sub(r'\d-(?=\d)', '', address)
    return address.strip()