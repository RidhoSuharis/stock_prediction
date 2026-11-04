import io

from flask import Blueprint, send_file

main_bp = Blueprint('main', __name__)


@main_bp.route('/download-template')
def download_template():

    csv_content = """Date;Close
2026-01-05;8250
2026-01-06;8300
2026-01-07;8275
2026-01-08;8350
2026-01-09;8400
"""

    file = io.BytesIO(csv_content.encode('utf-8'))
    file.seek(0)

    return send_file(
        file,
        mimetype='text/csv',
        as_attachment=True,
        download_name='template_data_saham.csv'
    )