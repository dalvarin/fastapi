from typing import Union

from fastapi import FastAPI

import ansible_runner

app = FastAPI()

@app.get("/")
def read_root():
    return {"hello":"world 2"}

@app.post("/launch/")
def launch_playbook(playbook_path:str, playbook_name:str ):
    # https://ansible.readthedocs.io/projects/runner/en/latest/
    # curl -X POST "http://192.168.56.101:8888/launch/?playbook_path=%2Fcode%2Fapp%2Fplaybooks&playbook_name=echo.yml"
    extravars = {'env':'DEV'}
    roles_path = '/code/ansible/roles'
    r = ansible_runner.run(private_data_dir=playbook_path, playbook=playbook_name, extravars=extravars, roles_path=roles_path)
    #r = ansible_runner.run(private_data_dir='/code/app/playbooks', playbook='echo.yml')
    events_list = list(r.events)
    # Se extrae el event_data de events - Es donde viene la informacion de ejecucion de las tareas entre otras cosas
    event_data_list = [event.get('event_data',{}) for event in events_list]
    # Filtramos por las entradas que sean de fin de tarea (con resultado)
    tasks_results = [item for item in event_data_list if ('res' in item)]
    # Buscamos la tarea en concreto
    tasks_results = [item for item in tasks_results if (item['task'] == 'Return role final result in suitable way and format')]
    print(tasks_results)
    print("Status: {}".format(r.status))
    print("Return code: {}".format(r.rc))
    print("Stats: {}".format(r.stats))
    #Si obtenemos el resultado de una tarea set_fact
    #final_json = tasks_results[0]['res']['ansible_facts']['ansible_final_output']
    # Si obtenemos el resultado de una tarea debug
    final_json = tasks_results[0]['res']['msg']
    # Si hemos lanzado varios hosts en el mismo playbook, bastaría con conseguir el resultado de la misma tarea de cada uno de hosts (en la tarea viene el host que es)
    print("REST API answer: {}".format(final_json))
    #Otra forma de conseguir datos de vuelta es con la fact_cache y filtrando por host
    #return r.get_fact_cache('localhost')
    return final_json

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}