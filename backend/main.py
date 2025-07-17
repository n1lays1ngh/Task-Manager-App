from fastapi import FastAPI
from models import Task,TaskCreate,TaskUpdate
from typing import List
from fastapi import HTTPException
from db import conn,cursor

app = FastAPI()



#Get all tasks
@app.get("/tasks",response_model = List[Task])
def get_tasks():
    cursor.execute("SELECT * FROM tasks")
    rows = cursor.fetchall()
    tasks = []

    for row in rows:
        
        task_dict = {
            "id": row["id"], # type: ignore
            "title": row["title"],  #type: IGNORE # type: ignore
            "description": row["description"],  # type: ignore
            "completed": row["completed"]  # type: ignore
        }
        tasks.append(task_dict)
    
    return tasks


    


#Create new tasks and add them
@app.post("/tasks")
def create_tasks(task:TaskCreate):
    try:
        cursor.execute("INSERT INTO tasks (title,description,completed) VALUES(%s, %s, %s) RETURNING * ",(task.title, task.description ,task.completed)
        )
        new_task = cursor.fetchone()
        conn.commit()
        return new_task
    
    except Exception as error:
        conn.rollback()
        raise HTTPException(status_code=500,detail=str(error))
    

    





#Get tasks by id

@app.get("/tasks/{task_id}",response_model=Task)
def get_tasks_id(task_id:int):
   
        cursor.execute("SELECT * FROM tasks WHERE id = %s",(task_id,))
        task = cursor.fetchone()
        

        if task is None:
             raise HTTPException(status_code=404,detail="Task not found")
        return task
    
    
    



#UPDATE Task
@app.put("/tasks/{task_id}")
def update_task(task_id:int,updated_task:TaskUpdate):
    try:
         
        cursor.execute("""
            UPDATE tasks
            SET title = %s , description = %s , completed = %s
            WHERE id = %s
            RETURNING * ;
        """ , (updated_task.title,updated_task.description,updated_task.completed,task_id))

        task = cursor.fetchone()
        conn.commit()

        if task is None :
            raise HTTPException(status_code=404,detail="Task not found")

        return task
    except Exception as error:
        conn.rollback()
        raise HTTPException(status_code=500,detail=str(error))



#DELETE tasks

@app.delete("/tasks/{task_id}")
def delete_tasks(task_id:int): 
    try:
        cursor.execute("""DELETE from tasks WHERE id = %s  RETURNING * """, (task_id,))
        deleted_task = cursor.fetchone()

        if deleted_task is None:
            raise HTTPException(status_code=404,detail="Task not found or Task does not exist")
        
        conn.commit()

        return {"message" : "Task Deleted" ,
                "deleted task " : deleted_task
                } 
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500,detail=str(e))
    




