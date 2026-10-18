from groq import Groq
import os 
import inspect
import json
from dotenv import load_dotenv
from typing import Literal,get_origin,get_args,cast
from groq.types.chat import ChatCompletionMessageParam
import argparse
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
parser = argparse.ArgumentParser()
parser.add_argument("--dev",action='store_true',help='Enable development/observability mode')
args=parser.parse_args()
dev_mode=args.dev
if dev_mode:
    print(
    Panel.fit(
        "[bold green]Status:[/bold green] Active\n[bold yellow]Dev Mode:[/bold yellow] ENABLED",
        title="[bold cyan]System Configuration[/bold cyan]",
        border_style="green",
    )
)
class DevLogger:
    def __init__(self, dev_mode:bool=False):
        self.dev_mode = dev_mode
        self.console = Console()

    def tool_call(self, name, arguments):
        if not self.dev_mode:
            return

        table = Table(show_header=False, box=None)

        table.add_row(
            "[bold]Tool[/bold]",
            f"[yellow]{name}[/yellow]"
        )

        table.add_row(
            "[bold]Arguments[/bold]",
            str(arguments)
        )

        self.console.print(
            Panel(
                table,
                title="[bold yellow]⚙ TOOL CALL[/bold yellow]",
                border_style="yellow",
            )
        )
    def model_request(self, messages):
        if not self.dev_mode:
            return
        to_add=[]
        for message in messages:
            role=message["role"]
            if message.get("content"):
                content=message["content"]
                req=f"{role}:\t{content}"
                to_add.append(req)
            elif message.get("tool_calls"):
                tool=message["tool_calls"]
                req=f"{role}:\t{tool}\n"
                to_add.append(req)   
            else:
                to_add.append(role)
        content='\n'.join(to_add)
        self.console.print(
            Panel(
                f"{content}",
                title="[bold cyan]MODEL REQUEST[/bold cyan]",
                border_style="cyan",
            )
        )
    def model_response(self, response):
        if not self.dev_mode:
            return

        self.console.print(
            Panel(
                str(response),
                title="[bold green]MODEL RESPONSE[/bold green]",
                border_style="green",
            )
        )
    def tool_result(self, result):
        if not self.dev_mode:
            return

        self.console.print(
            Panel(
                str(result),
                title="[bold magenta]TOOL RESULT[/bold magenta]",
                border_style="magenta",
            )
        )
dev_logger=DevLogger(dev_mode)
load_dotenv()
api=os.getenv("Groq_API")
client=Groq(api_key=api)
dev=False
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
    dev_logger.tool_call(func_name,func_param)
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
user_question=str(input("Enter your question."))

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
dev_logger.model_request(messages)
print("user:\t",user_question)      
def call_groq(messages):  
    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=messages,
        tools=Tools
    )
    dev_logger.model_response(response.choices[0].message)
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
        try:
            tool_answer = tool_caller(tools_call)
        except KeyError:
            tool_answer="Tool not found!"
        except (TypeError,ValueError):
            tool_answer="Invalid arguments were given."
        dev_logger.tool_result(tool_answer)

        tool_to_model: ChatCompletionMessageParam = {
            "role": "tool",
            "tool_call_id": tools_call.id,
            "content": str(tool_answer)
        }

        messages.append(tool_to_model)
        
    dev_logger.model_request(messages)
    response = call_groq(messages)
    message = response.choices[0].message
print("assistant\t",message.content)
