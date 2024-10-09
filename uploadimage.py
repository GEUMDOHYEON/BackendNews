from fastapi import UploadFile, File
import uuid
from PIL import Image, ImageOps
from fastapi import UploadFile, HTTPException, status
from datetime import datetime

# File을 그냥 Optional로 지정했음
async def upload_image(folder_name, file: UploadFile | None = File(None)):
    """
    이미지 업로드 
    - 1. 클라이언트에서 서버로 이미지를 업로드한다.
    - 2. 이미지 확장자가 업로드 가능한지 확인한다.
    - 3. 이미지 사이즈가 업로드 가능한 크기인지 확인한다.
    - 4. 이미지 이름을 변경한다.
    - 5. 이미지를 최적화하여 저장한다.
    - 반환: original_filename, modified_filename, filepath
    """
    if not file:
        return {"detail": "이미지 없음"}
 
    file = await validate_image_type(file)
    file = await validate_image_size(file)
    original_filename = file.filename
    file = change_filename(file)
    modified_filename = file.filename
    image = resize_image(file)
    file_path = f"./static/{folder_name}/{modified_filename}"
    image = save_image_to_filesystem(image, file_path)
    return {
        "original_filename": original_filename,
        "modified_filename": modified_filename,
        "filepath": file_path,
        "detail": "이미지 업로드 성공"
    }


# 이미지 파일 확장자/타입 확인
async def validate_image_type(file: UploadFile) -> UploadFile:
    # jpg, jpeg, png만 가능
    if file.filename.split(".")[-1].lower() not in ["jpg", "jpeg", "png"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="업로드 불가능한 이미지 확장자입니다.",
        )
    
    # 파일 타입 확인(image)
    if not file.content_type.startswith("image"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="이미지 파일만 업로드 가능합니다.",
        )
    return file


# 이미지 업로드 파일크기 확인
async def validate_image_size(file: UploadFile) -> UploadFile:
    if len(await file.read()) > 10 * 1024 * 1024:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="이미지 파일은 10MB 이하만 업로드 가능합니다.",
        )
    return file

# 이미지 파일 이름 수정
def change_filename(file: UploadFile) -> UploadFile:
    """
    이미지 이름 변경
    """
    uuid_name = uuid.uuid4()
    now_date = datetime.now().strftime("%Y%m%d%H%M")
    file.filename = f"{uuid_name}_{now_date}.jpeg"
    return file

# 일정 비율로 축소
def resize_image(file: UploadFile, max_size: int = 1024):
    read_image = Image.open(file.file)
    original_width, original_height = read_image.size
    
    # 최대 사이즈보다 클시
    if original_width > max_size or original_height > max_size:
        if original_width > original_height:
            new_width = max_size
            new_height = int((new_width / original_width) * original_height)
        else:
            new_height = max_size
            new_width = int((new_height / original_height) * original_width)
        read_image = read_image.resize((new_width, new_height))
    
    # png 경우 RGBA 형태기에 RGB저장
    read_image = read_image.convert("RGB")
    # 올바른 방향으로 조정
    read_image = ImageOps.exif_transpose(read_image)
    return read_image
 
def save_image_to_filesystem(image: Image, file_path: str):
    image.save(file_path, "jpeg", quality=70)
    return file_path