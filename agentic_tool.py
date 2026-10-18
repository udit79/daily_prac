from enum import Enum
class Status(Enum):
    pending="pending"
    completed="completed"
tasks = [
    {
        "id": 1,
        "title": "Complete binary tree assignment",
        "subject": "DSA",
        "topic": "Trees",
        "status": "pending"
    },
    {
        "id": 2,
        "title": "Revise Python decorators",
        "subject": "Python",
        "topic": "Advanced Python",
        "status": "completed"
    },
    {
        "id": 3,
        "title": "Implement FastAPI validation",
        "subject": "Backend",
        "topic": "FastAPI",
        "status": "pending"
    }
]
def search_tasks(query:str, subject:str|None=None, status:Status|None=None, top_k:int=5):
    if top_k<=0:
        return []
    if not query.strip():
        return []
    matching_result=[]
    query=query.strip().lower()
    query_tokens=query.split()
    for task in tasks:
        pt=0
        task_text=(task["title"].strip()+""+task["topic"].strip()).lower()
        for token in query_tokens:
            if token in task_text:
                pt+=1
        relevance=pt/len(query_tokens)
        if relevance==0:
            continue
        if subject and subject.lower().strip()!=task["subject"].lower().strip():
            continue
        if status and status.value!=task["status"]:
            continue
        if relevance>0:
            task_with_points=task.copy()
            task_with_points['relevance']=relevance
            matching_result.append(task_with_points)
    matching_result.sort(key=lambda x:x["relevance"],reverse=True) 
    unique_data=[]
    seen=set() 
    for task in matching_result:
        task.pop("relevance",None)
        if task["id"]  not in seen:
            seen.add(task["id"])
            unique_data.append(task)

    return unique_data[:top_k]
print(search_tasks(query="Python"))