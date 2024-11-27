from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
import io
import csv
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.requests import Request
import uvicorn
from parser.parser import parser
import time

app = FastAPI()
templates = Jinja2Templates(directory="templates")


@app.get(f'/', response_class=HTMLResponse)
async def resumes(request: Request):
    return templates.TemplateResponse('in2.html', {"request": request})

@app.get(f'/dash', response_class=HTMLResponse)
async def resumes(request: Request):
    return templates.TemplateResponse('dashboard.html', {"request": request})

@app.post("/generate-csv")
async def generate_csv(input_data: dict):
    try:
        time.sleep(1)
        data = input_data.get("input_data")
        if not data:
            raise HTTPException(status_code=400, detail="No input data provided")

        # Генерація CSV у пам'яті
        csv_file = io.StringIO()
        writer = csv.writer(csv_file)
        writer.writerow(["Input Data", "Processed Result"])
        writer.writerow([data, f"Processed: {data}"])

        # Повернення файлу як стрім
        csv_file.seek(0)
        response = StreamingResponse(
            csv_file,
            media_type="text/csv",
            headers={"Content-Disposition": "attachment; filename=parsed_data.csv"},
        )
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get(f'/parser', response_class=HTMLResponse)
async def resumes(request: Request):
    li = parser()
    return templates.TemplateResponse('parserHTMX.html', {
            "request": request,
            "li": li,
        })

if __name__ == "__main__":
     uvicorn.run(app, host="0.0.0.0", port=7000)