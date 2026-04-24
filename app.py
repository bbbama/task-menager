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

@app.route("/tasks/<int:task_id>/complete", methods=["POST"])
def complete_task(task_id):
    tasks = load_tasks()

    for task in tasks:
        if task["id"] == task_id:
            task["done"] = True
            save_tasks(tasks)
            return jsonify(task)

    return jsonify({"error": "Task not found"}), 404

if __name__ == "__main__":
    app.run(debug=True)
