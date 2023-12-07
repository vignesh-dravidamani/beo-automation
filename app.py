import json
from typing import Union
from fastapi import FastAPI, UploadFile, Response

from db import vdb_insert
from util import extract_menu_items, color_code_menu_items
from llm import query_ai

app = FastAPI()


@app.post("/color")
async def color(file: Union[UploadFile, None] = None):
    if not file:
        return {"message": "No BEO file sent"}
    else:
        contents = file.file.read()
        menu_items = json.loads(query_ai(extract_menu_items(contents)))
        color_coded_contents = color_code_menu_items(contents, menu_items)
        headers = {'Content-Disposition': 'inline; filename=' + file.filename}
        return Response(color_coded_contents, headers=headers, media_type='application/pdf')

