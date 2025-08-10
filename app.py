from fastapi import FastAPI, File, UploadFile
from fastapi.responses import StreamingResponse
from rembg import remove
from io import BytesIO
from PIL import Image
import uvicorn

app = FastAPI()

@app.get("/")
def home():
    return {"status": "Pixora BG Remover API is running 🚀"}

@app.post("/remove-bg")
async def remove_bg(file: UploadFile = File(...)):
    # read uploaded file bytes
    input_image = await file.read()
    # rembg returns raw PNG bytes (with alpha)
    output_image = remove(input_image)

    # ensure it's a PNG streamable via StreamingResponse
    img = Image.open(BytesIO(output_image)).convert("RGBA")
    buf = BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)

    return StreamingResponse(buf, media_type="image/png")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
