import time

from flask import Flask, request, jsonify
from Yandex_map_parser import YandexMapParser
import functions

app = Flask(__name__)


@app.route('/get_location', methods=['GET'])
def get_location():
    address = request.args.get('address')
    house_number = request.args.get('house_number')
    if not address:
        return jsonify({"error": "Address parameter is required"}), 400
    if not house_number:
        return jsonify({"error": "house_number parameter is required"}), 400

    location_from_NOMI = functions.get_location(functions.clean_address(address))

    if location_from_NOMI:
        return jsonify(location_from_NOMI)
    else:


        # Максимальное количество попыток
        max_attempts = 3
        for attempt in range(max_attempts):
            parser = YandexMapParser()
            location = parser.get_location_from_Yandex(functions.modify_address_for_Yandex(address))

            if location == None:
                parser.close_browser()
                return jsonify({"error": "Location not found"}), 404
            else:

                # Проверяем наличие ключа 'input_not_found' и его значение
                if not location['Input_not_found']:
                    parser.close_browser()
                    if functions.check_address_correct(address, house_number):
                        return jsonify([float(location['latitude']), float(location['longitude'])])
                    else:
                        return jsonify({"error": "Location not found"}), 404

            # Если 'input_not_found' = True, ждем 3 секунд и пробуем снова
            parser.close_browser()
            time.sleep(5)


        # Если после всех попыток результат тот же, возвращаем ошибку
        return jsonify({"error": "Location not found. Maybe scrip got capcha!"}), 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)