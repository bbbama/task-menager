from flask import Flask, request, jsonify
import json

app = Flask(__name__)

TASKS_FILE = "tasks.json"

def load_tasks():
    try:
        with open(TASKS_FILE, "r") as f:
            return json.load(f)
    except:
        return []

def save_tasks(tasks):
    with open(TASKS_FILE, "w") as f:
        json.dump(tasks, f)

@app.route("/tasks", methods=["GET"])
def get_tasks():
    return jsonify(load_tasks())

@app.route("/tasks", methods=["POST"])
def add_task():
    tasks = load_tasks()
    data = request.json

    task = {
        "id": len(tasks) + 1,
        "title": data.get("title"),
        "done": False
    }

    tasks.append(task)
    save_tasks(tasks)

    return jsonify(task), 201

if __name__ == "__main__":
    app.run(debug=True)
