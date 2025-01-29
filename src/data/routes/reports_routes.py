from flask import Blueprint, request, jsonify
from datetime import datetime
from reporting import generate_reports  # Oletetaan, että olet muuttanut pääohjelman funktioksi nimeltä generate_reports

report_bp = Blueprint('report', __name__)

@report_bp.route('/reports', methods=['POST'])
def generate_report():
    try:
        # Tarkistetaan, että pyyntö sisältää JSON-dataa
        data = request.get_json()

        if data is None:
            # Jos data on tyhjä, asetetaan oletusarvot
            year = datetime.now().year
            start_month = datetime.now().month
            end_month = start_month  # Jos ei ole määritetty end_month, se on sama kuin start_month
        else:
            try:
                year = int(data.get('year', datetime.now().year))
                start_month = int(data.get('start_month', datetime.now().month))
                end_month = int(data.get('end_month', start_month))
            except ValueError:
                return jsonify({"error": "Invalid input, year and months must be integers"}), 400

        # Kutsutaan raportin generointifunktiota
        report_file = generate_reports(year, start_month, end_month, upload_to_blob=True)

        # Palautetaan raportin nimi vastauksena
        return jsonify({"message": f"Reports generated: {report_file}"}), 200
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500