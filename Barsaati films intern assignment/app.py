from flask import Flask, render_template, jsonify
import threading
from scrape_twitter import fetch_trending_topics

app = Flask(__name__)

latest_result = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/fetch-trending')
def fetch_trending():
    def run_script():
        global latest_result
        latest_result = fetch_trending_topics()
    
    thread = threading.Thread(target=run_script)
    thread.start()
    thread.join()  # Wait for the thread to complete
    
    return jsonify(latest_result)

if __name__ == '__main__':
    app.run(debug=True)
