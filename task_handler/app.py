import json
import uuid
from models.entities.Task import Task
from models.TaskModel import TaskModel

task_path = '/task'
tasks_path = '/tasks'


def lambda_handler(event, context):
    response = None

    try:
        http_method = event.get('httpMethod')
        path = event.get('path')

        if http_method == 'GET' and path == tasks_path:
            user_id = event['queryStringParameters']['userId']
            response = get_tasks_by_user(user_id)
        elif http_method == 'POST' and path == task_path:
            response = add_task(json.loads(event['body']))
        elif http_method == 'PATCH' and path == task_path:
            id = event['queryStringParameters']['id']
            response = update_task(id, json.loads(event['body']))
        elif http_method == 'DELETE' and path == task_path:
            id = event['queryStringParameters']['id']
            response = delete_task(id)
        else:
            response = build_response(404, '404 Not Found')
    
    except Exception as e:
        print('Error:', e)
        response = build_response(400, 'Error processing request')

    return response

def get_tasks_by_user(user_id):
    tasks = TaskModel.get_tasks_by_user(user_id)
    return build_response(200, tasks)


def add_task(request_body):
    id = uuid.uuid4()
    name = request_body['name']
    description = request_body['description']
    user_id = request_body['user_id']
    task = Task(str(id), name, description, user_id)
    TaskModel.add_task(task)
    return build_response(201, 'Task added successfully')


def update_task(id, request_body):
    name = request_body['name']
    description = request_body['description']
    status = request_body['status']
    print(f"status: {status}")

    task = Task(id, name, description, bool(status), status)
    affected_rows = TaskModel.update_task(task)

    if affected_rows == 1:
        return build_response(200, task.id)
    else:
        return build_response(404, 'Not found')


def delete_task(id):
    tasks = TaskModel.delete_task(id)
    return build_response(200, tasks)


def build_response(status_code, body):
    return {
        'statusCode': status_code,
        'headers': {
            'Content-Type': 'application/json'
        },
        'body': json.dumps(body)
    }