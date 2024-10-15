from fastapi import FastAPI
from requests import get as get_request
from dateutil import parser as date_parse
from datetime import datetime as dt
from datetime import timedelta as td 

import uvicorn

app = FastAPI()


@app.get("/bus_location/{bus_name}")
async def get_bus_location(bus_name):

    if bus_name == "gorod":
        bus_id = gorod_bus_id
    if bus_name == "kon":
        bus_id = konovalovka_bus_id

    get_online_info_link = f"http://{service_ip}/ServiceJSON/GetOnlineInfo?session={session}&schemaID={schema_id}&IDs={bus_id}"
    
    get_info = get_request(f"{get_online_info_link}").json()
    
    last_time = date_parse.parse(get_info[bus_id]["LastData"])+td(hours=3)

    return {"bus_name":   get_info[bus_id]["Name"],
            "latitude":   get_info[bus_id]["LastPosition"]["Lat"],
            "longitude":  get_info[bus_id]["LastPosition"]["Lng"],
            "time":       dt.strftime(last_time, '%d-%m-%Y %H:%M:%S')}


@app.get("/")
async def root():
    return {"message": "Hello World"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=80, reload=True)