from sqlalchemy.orm import Session
from app.schemas.course_module import CourseModulesCreate, ModuleHeader
from app.crud.course_module import (
    create_course_modules,
    get_modules_by_course,
    update_module_header
)

class ModuleService:

    @staticmethod
    def create_headers(db: Session, payload: CourseModulesCreate):
        return create_course_modules(db, payload)

    @staticmethod
    def get_by_course(db: Session, course_id: int):
        return get_modules_by_course(db, course_id)

    @staticmethod
    def update_header(db: Session, module_id: int, payload: ModuleHeader):
        return update_module_header(db, module_id, payload)
