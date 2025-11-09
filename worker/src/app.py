import threading
from flask import Flask, jsonify
from uuid import UUID, uuid4
from worker import run_worker
import model # Import the model module to use its functions


app = Flask(__name__)

# Start the worker in a background thread
worker_thread = threading.Thread(target=run_worker, daemon=True)
worker_thread.start()



@app.route("/jobs/<string:job_id>/related", methods=["GET"])
def get_related_jobs(job_id):
    try:
        # Check if job_id is a valid UUID
        uuid_obj = UUID(job_id)

    except ValueError:
        return jsonify({"error": "Invalid job ID format"}), 400

    related_jobs = model.get_related_jobs(uuid_obj)
    return jsonify(related_jobs)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)