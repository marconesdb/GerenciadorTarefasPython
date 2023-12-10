# app/routes.py
from flask import render_template, request, redirect, url_for
from app import app

tasks = []

priority_labels = {
    1: "Crítica",
    2: "Urgente",
    3: "Média",
    4: "Importante",
    5: "Baixa",
}

status_labels = {
    'pending': "Pendente",
    'completed': "Concluída",
}

@app.route('/')
def index():
    tasks.sort(key=lambda x: x['priority'])
    return render_template('index.html', tasks=tasks, priority_labels=priority_labels, status_labels=status_labels)
# ...

@app.route('/add_task', methods=['POST'])
def add_task():
    description = request.form['description']
    due_date = request.form['due_date']
    priority = int(request.form['priority'])
    status = 'Pendente'
    note = request.form.get('note', '')  # Adicionado para capturar a observação ou usar uma string vazia se não houver

    if 1 <= priority <= 5:
        tasks.append({'description': description, 'due_date': due_date, 'priority': priority_labels[priority], 'status': status, 'note': note})

    return redirect(url_for('index'))

# ...


@app.route('/complete_task/<int:task_id>')
def complete_task(task_id):
    global tasks
    if 0 <= task_id < len(tasks):
        tasks[task_id]['status'] = 'Concluída'
    return redirect(url_for('index'))

# ... (restante do código)

@app.route('/delete_task/<int:task_id>')
def delete_task(task_id):
    global tasks
    tasks = [task for task in tasks if tasks.index(task) != task_id]
    return redirect(url_for('index'))

@app.route('/edit_task/<int:task_id>')
def edit_task(task_id):
    task = tasks[task_id]
    return render_template('edit_task.html', task=task, task_id=task_id, priority_labels=priority_labels)

@app.route('/update_task/<int:task_id>', methods=['POST'])
def update_task(task_id):
    global tasks
    description = request.form['description']
    due_date = request.form['due_date']
    priority = int(request.form['priority'])

    if 1 <= priority <= 5:
        tasks[task_id] = {'description': description, 'due_date': due_date, 'priority': priority_labels[priority]}

    return redirect(url_for('index'))