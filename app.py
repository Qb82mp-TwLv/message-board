from fastapi import *
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv
from dbUsing import db_interaction
import boto3, os, hashlib
from datetime import datetime


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
async def index(request: Request):
    return FileResponse("./static/index.html", media_type="text/html")

db = db_interaction()
@app.post("/api/comment")
async def upload_comment(comment_text:str = Form(), image: UploadFile=File(...)):
    try:
        # 避免名稱相同的問題
        name, extension = os.path.splitext(image.filename)
        hash_name = hashlib.sha256(name.encode('utf-8')).hexdigest()[:10]
        time_number = datetime.now().strftime("%Y%m%d%H%M%S")
        key_name = f"img_{hash_name}_{time_number}{extension}"
        
        # # 儲存評價的文字
        _result = await db.create_comment_info(comment_text, key_name)
        if _result == True:
            # 確認檔案類行為image
            if not image.content_type.startswith("image/"):
                return {"error": "請根據提供的方式進行操作"}
            else:
                file_size = await image.read()
                if len(file_size) > (5*1024*1024):
                    return {"error": "圖片檔案過大。"}
                image.file.seek(0)

                load_dotenv()
                bucket_name = os.getenv("API_AWS_BUCKET_NAME")

                s3 = boto3.client("s3")
                s3.upload_fileobj(
                    Fileobj = image.file,
                    Bucket=bucket_name,
                    Key="commtest/"+key_name,
                    ExtraArgs={"ContentType": image.content_type}
                )

                return {"result": True}
        
        return {"error": "請根據提供的方式進行操作"}
    except Exception:
        return {"error": "請根據提供的方式進行操作"}

@app.get("/api/comment")
async def get_comment(times:int):
    _result = await db.query_comment_info(times)
    try:
        load_dotenv()
        path = os.getenv("API_AWS_CDN_PATH")
        url = f"{path}/"

        if _result != False:
            data_json = []
            if times == 1:
                for comm, imgName, in _result:
                    imgUrl = url+imgName

                    info = {"comment": comm, "image_name": imgUrl}
                    data_json.append(info)
            elif times == 2:
                comm, imgName = _result
                imgUrl = url+imgName

                info = {"comment": comm, "image_name": imgUrl}
                data_json.append(info)

            if data_json != []:
                return {"result": data_json}
            
        return {"error": "請根據提供的方式進行操作"}
    except Exception:
        return {"error": "請根據提供的方式進行操作"}


    