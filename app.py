import io
from flask import Flask, request, send_file, jsonify
from playwright.sync_api import sync_playwright

app = Flask(__name__)

@app.route('/render', methods=['POST'])
def render():
    data = request.get_json(force=True)
    html = data.get('html')
    width = data.get('width', 894)
    height = data.get('height', 1264)
    scale = data.get('scale', 3)

    if not html:
        return jsonify({'error': 'html required'}), 400

    try:
        # har request ke andar hi browser start karo, aur band kar do
        with sync_playwright() as p:
            browser = p.chromium.launch(
                args=['--no-sandbox', '--disable-gpu', '--hide-scrollbars']
            )
            context = browser.new_context(
                viewport={'width': width, 'height': height},
                device_scale_factor=scale
            )
            page = context.new_page()
            page.set_content(html, wait_until='load', timeout=60000)
            img_bytes = page.screenshot(full_page=True, type='png')
            browser.close()
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    return send_file(
        io.BytesIO(img_bytes),
        mimetype='image/png',
        as_attachment=False,
        download_name='render.png'
    )

@app.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
