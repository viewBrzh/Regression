from fastapi import APIRouter, HTTPException
from fastapi.responses import HTMLResponse, FileResponse

router = APIRouter()

def read_html_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    return content

@router.get("/redwine_view/index", response_class=HTMLResponse)
def read_wine_index_html():
    html_file_path = "web/wine/index.html"  # Update the path to your Wine-related HTML files
    html_content = read_html_file(html_file_path)
    return html_content

@router.get("/redwine_view/insert", response_class=HTMLResponse)
def read_wine_insert_html():
    html_file_path = "web/wine/insert.html"  # Update the path to your Wine-related HTML files
    html_content = read_html_file(html_file_path)
    return html_content

@router.get("/redwine_view/update", response_class=HTMLResponse)
def read_wine_update_html():
    html_file_path = "web/wine/update.html"  # Update the path to your Wine-related HTML files
    html_content = read_html_file(html_file_path)
    return html_content

@router.get("/redwine_view/predict", response_class=HTMLResponse)
def read_wine_predict_html():
    html_file_path = "web/wine/predict.html"  # Update the path to your Wine-related HTML files
    html_content = read_html_file(html_file_path)
    return html_content
