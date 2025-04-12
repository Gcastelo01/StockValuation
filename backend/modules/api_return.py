from io import BytesIO
from pydantic import BaseModel



class AnalysisReturn(BaseModel):
    file: BytesIO