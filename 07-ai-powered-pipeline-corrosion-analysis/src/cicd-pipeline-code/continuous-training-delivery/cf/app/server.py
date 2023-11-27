from flask import Flask, request, jsonify
from flask_cors import CORS
from ct_cd_pipeline import ct_cd_pipeline

app = Flask(__name__)
CORS(app)

pipeline = ct_cd_pipeline()

@app.route('/', methods=['GET'])
def root():
    return 'Pipeline APIs are all healthy', 200

@app.route("/run_workflow", methods=["POST"])
def run_workflow():
    try:
        # Call the run_workflow function from your ct_cd_pipeline instance
        pipeline.run_workflow()
        return jsonify({"message": "Workflow executed successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run('0.0.0.0', 8080)