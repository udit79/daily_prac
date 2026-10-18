from pathlib import Path
from typing import Annotated,Literal
import json
from pydantic import BaseModel,StringConstraints,Field,ValidationError,StrictInt,StrictFloat
class json_line_check(BaseModel):
    request_id:Annotated[str,StringConstraints(strip_whitespace=True,min_length=1)]
    model:Annotated[str,StringConstraints(strip_whitespace=True,min_length=1)]
    status:Literal["success","error","timeout"]
    latency_ms:Annotated[StrictInt|StrictFloat,Field(ge=0,allow_inf_nan=False)]
def check_jsonl(json_line:dict)->dict|str:
    try:
        validated_model=json_line_check(**json_line)
        validated_dict=validated_model.model_dump()
        return validated_dict
    except ValidationError as e:
        return e.errors()[0]["msg"]
def convert_dict(string_data:str)->dict|str|ValueError|TypeError:
    try:
        converted_dict=json.loads(string_data)
        return converted_dict
    except (ValueError,TypeError) as e:
        return e
def analyse_infrence_log(path:str|Path)->dict[str,object]:
    if isinstance(path,str):
        working_path=Path.joinpath(Path.cwd(),path)
    else:
        working_path=path
    final_records:dict={"status_counts":{},"model_counts":{},"errors":{}}
    with open(working_path,"r",encoding="utf-8") as f:
        for index,line in enumerate(f,start=1):
            output=convert_dict(line)
            if not line.strip():
                continue
            elif not isinstance(output,dict):
                final_records["invalid_records"]=final_records.get("invalid_records",0)+1
                if len(final_records["errors"])<5:
                    if not isinstance(output,(ValueError,TypeError,str)):
                        final_records["errors"][index]=f"dict was expected but {output} is given."
                    elif isinstance(output,(ValueError,TypeError)):
                        final_records["errors"][index]=f"Provide a valid json."
                    else:
                        final_records["errors"][index]="Expected a JSON object, but got a string."
            else:
                err=check_jsonl(output)
                if isinstance(err,dict):
                    final_records["valid_records"]=final_records.get("valid_records",0)+1
                    final_records["status_counts"][err["status"]]=final_records["status_counts"].get(err["status"],0)+1
                    final_records["model_counts"][err["model"]]=final_records["model_counts"].get(err["model"],0)+1
                    final_records["average_latency_ms"]=final_records.get("average_latency_ms",0)+err["latency_ms"]
                else:
                    if len(final_records["errors"])<5:
                        final_records["errors"][index]=err
                    final_records["invalid_records"]=final_records.get("invalid_records",0)+1
    if final_records.get("valid_records",0)!=0:
        final_records["average_latency_ms"]=final_records["average_latency_ms"]/final_records["valid_records"]
        try:
            final_records["invalid_records"]
        except KeyError:
            final_records["invalid_records"]=0
    else:
        final_records["average_latency_ms"]=None
        try:
            final_records["valid_records"]
        except KeyError:
            final_records["valid_records"]=0
        try:
            final_records["invalid_records"]
        except KeyError:
            final_records["invalid_records"]=0
    return final_records
print(analyse_infrence_log("test.jsonl"))