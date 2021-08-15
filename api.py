from typing import Optional

from fastapi import APIRouter

from utils import String

router = APIRouter(prefix="/api")


@router.get("/string/{open_note}")
def return_string(open_note: Optional[str] = 'E0'):
    return String(open_note)
