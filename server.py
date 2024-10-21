from flask import Flask, request, jsonify
from Yandex_map_parser import YandexMapParser
import functions
import time

app = Flask(__name__)
parser = YandexMapParser()

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
        location = parser.get_location_from_Yandex(functions.modify_address_for_Yandex(address))

        if location is None:
            parser.clear_cookies()
            parser.restart_browser()
            return jsonify({"error": "Location not found"}), 404
        else:
            if not location['Input_not_found']:
                if functions.check_address_correct(location['Yandex_address'], house_number):
                    return jsonify([float(location['latitude']), float(location['longitude'])])
                else:
                    return jsonify({"error": "Location not found"}), 404

        time.sleep(5)  # Подождите перед повторной попыткой
        return jsonify({"error": "Location not found. Maybe script got captcha!"}), 404

if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', port=8080)
    finally:
        parser.stop_browser()  # Убедитесь, что Xvfb остановлен при выходе