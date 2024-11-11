from typing import Union

from fastapi import FastAPI

import ansible_runner

app = FastAPI()

@app.get("/")
def read_root():
    return {"hello":"world"}

@app.post("/launch/")
def launch_playbook(playbook_path:str, playbook_name:str ):
    # https://ansible.readthedocs.io/projects/runner/en/latest/
    # curl -X POST "http://192.168.56.101:8888/launch?playbook_path=%2Fcode%2Fapp%2Fplaybooks&playbook_name=echo.yml"
    r = ansible_runner.run(private_data_dir=playbook_path, playbook=playbook_name)
    #r = ansible_runner.run(private_data_dir='/code/app/playbooks', playbook='echo.yml')
    events_list = list(r.events)
    # Se extrae el event_data de events - Es donde viene la informacion de ejecucion de las tareas entre otras cosas
    event_data_list = [event.get('event_data',{}) for event in events_list]
    # Filtramos por las entradas que sean de fin de tarea (con resultado)
    tasks_results = [item for item in event_data_list if ('res' in item)]
    # Buscamos la tarea en concreto
    tasks_results = [item for item in tasks_results if (item['task'] == 'Establecemos json a devolver')]
    print(tasks_results)
    print("Status: {}".format(r.status))
    print("Return code: {}".format(r.rc))
    print("Stats: {}".format(r.stats))
    final_json = tasks_results[0]['res']['ansible_facts']['ansible_final_output']
    print("REST API answer: {}".format(final_json))
    #return r.get_fact_cache('localhost')
    return final_json


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}