from groq import Groq
import os 
import inspect
import json
from dotenv import load_dotenv
from typing import Literal,get_origin,get_args,cast
from groq.types.chat import ChatCompletionMessageParam
load_dotenv()
api=os.getenv("Groq_API")
client=Groq(api_key=api)
def python_to_json(annotation):
    origin=get_origin(annotation)
    if origin is Literal:
        value=get_args(annotation)
        return {
            "type":"string",
            "enum":list(value)
        }
    type_mapping = {
        str: "string",
        int: "integer",
        float: "number",
        bool: "boolean"
    }
    if annotation in type_mapping:
        return{
            "type":type_mapping[annotation]
        }
    raise TypeError(f"Unsupported type: {annotation}")

Tools=[]
tool_registry={}
def tool(func):
    signature=inspect.signature(func)
    properties={}
    required=[]
    for name,param in signature.parameters.items():
        if param.kind in (
            inspect.Parameter.VAR_POSITIONAL,
            inspect.Parameter.VAR_KEYWORD
        ):
            continue
        properties[name]=python_to_json(param.annotation)
        if param.default is inspect.Parameter.empty:
            required.append(name)
    tool_schema={
        "type":"function",
        "function":{
            "name":func.__name__,
            "description":inspect.getdoc(func),
            "parameters":{
                "type":"object",
                "properties":properties,
                "required":required
            }
        }
    }
    Tools.append(tool_schema)
    tool_registry[func.__name__] = func
    return func
def tool_caller(tool_reply):
    func_name=tool_reply.function.name
    func_param=json.loads(tool_reply.function.arguments)
    if func_name in tool_registry:
        func=tool_registry[func_name]
        return func(**func_param)
    else:
        return "Something went wrong cant call the tool."
    

@tool
def calculator(a:float,b:float,operation:Literal["add","multiply","subtract","divide"])->float:
    """
    It takes two numbers(a,b) and an operaton.The operations that can be passed are:["add","multiply","subtract","divide"].According to the operation passed into function it performs the action.
    """
    match operation:
        case "add":
            return a+b
        case "multiply":
            return a*b
        case "subtract":
            return a-b
        case "divide":
            if b==0:
                raise ValueError("Can't divide by zero.")
            return a/b
@tool
def get_string_length(a:str)->int:
    """
    It takes a string and returns its length.
    """
    return len(a)
@tool
def is_even(a: int) -> bool:
    """
    Takes an integer and returns whether it is even.
    """
    return a % 2 == 0
user_question="Calculate 125 + 75 and tell me whether the result is even."
messages:list[ChatCompletionMessageParam]=[
        {
            "role": "system",
            "content": "Use the calculator tool when mathematical calculation is required."
        },
        {
            "role": "user",
            "content": user_question
        }
] 
print("user\t",user_question)      
def call_groq(messages):  
    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=messages,
        tools=Tools
    )
    return response
response=call_groq(messages)
message=response.choices[0].message
    
while message.tool_calls:
    model_reply = cast(
        ChatCompletionMessageParam,
        message.model_dump(mode="json", exclude_none=True)
    )
    messages.append(model_reply)

    for tools_call in message.tool_calls:
        tool_answer = tool_caller(tools_call)

        tool_to_model: ChatCompletionMessageParam = {
            "role": "tool",
            "tool_call_id": tools_call.id,
            "content": str(tool_answer)
        }

        messages.append(tool_to_model)

    response = call_groq(messages)
    message = response.choices[0].message
print("assistant\t",message.content)
