from fastapi import FastAPI, HTTPException
from typing import Optional,List,Dict
from pydantic import BaseModel
from datetime import date
import json
from os import listdir
from os.path import isfile, join

class Details(BaseModel):
    cuisine_type: str

class Restaurant(BaseModel):
    restaurant_id: int
    details:  Optional[Details] = None
    name: str 
    street_address: str
    city: str
    state: str
    postal_code: str

class Violation(BaseModel):
    violation_id: int
    is_critical: bool
    is_repeat: Optional[bool] = None
    is_corrected_on_site: Optional[bool] = None
    code: int
    description: str
    comments: str

class Inspection(BaseModel):
    inspection_id: int
    inspection_date: str
    score: int
    comments: str
    type: Optional[str] = None
    violations: Optional[List[Violation]] = None
    restaurant: Optional[Restaurant]



app = FastAPI()


@app.post("/load_inspection")
def post_inspection(inspection:Inspection):
    if inspection.score > 100 or inspection.score < 0:
        raise HTTPException(status_code=404, detail="inspection score is not valid")
    elif inspection.violations is None:
        raise HTTPException(status_code=404, detail="Violations array does not exist")
    elif inspection.restaurant.city == '':
        raise HTTPException(status_code=404, detail="Restaurant city missing")
    elif inspection.restaurant.name == '':
        raise HTTPException(status_code=404, detail="Restaurant name missing")
    elif len(inspection.restaurant.state) != 2:
        raise HTTPException(status_code=404, detail="Restaurant state code invalid")
    else:
        ins_id = inspection.inspection_id            
        inspection_dict = inspection.dict()
        with open('processed/inspection_{}.json'.format(ins_id),"w") as file:
            json.dump(inspection_dict,file)
        return inspection


@app.get("/get_inspection/{ins_id}")
def get_inspection(ins_id:str):
    file_wanted = 'processed/inspection_{}.json'.format(ins_id)
    if isfile(file_wanted) is True:
        with open(file_wanted,"r") as file:
            out_file = json.load(file)
        return out_file


