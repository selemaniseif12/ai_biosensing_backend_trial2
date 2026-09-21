from sqlalchemy.orm import Session
from app.models.course_module import CourseModule
from app.schemas.course_module import CourseModulesCreate, ModuleHeader

def create_course_modules(db: Session, payload: CourseModulesCreate):
    created_modules = []

    for module in payload.modules:
        db_module = CourseModule(
            course_id=payload.course_id,
            module_number=module.module_number,
            title=module.title,
            description=module.description,
            has_lessons=module.has_lessons,
            has_quizzes=module.has_quizzes,
            has_assignments=module.has_assignments,
            has_videos=module.has_videos,
            has_slides=module.has_slides,
            has_pdfs=module.has_pdfs,
            has_websites=module.has_websites
        )
        db.add(db_module)
        created_modules.append(db_module)

    db.commit()
    for m in created_modules:
        db.refresh(m)

    return created_modules


def get_modules_by_course(db: Session, course_id: int):
    return db.query(CourseModule).filter(CourseModule.course_id == course_id).all()


def update_module_header(db: Session, module_id: int, module: ModuleHeader):
    db_module = db.query(CourseModule).filter(CourseModule.id == module_id).first()
    if not db_module:
        return None

    db_module.module_number = module.module_number
    db_module.title = module.title
    db_module.description = module.description

    db_module.has_lessons = module.has_lessons
    db_module.has_quizzes = module.has_quizzes
    db_module.has_assignments = module.has_assignments
    db_module.has_videos = module.has_videos
    db_module.has_slides = module.has_slides
    db_module.has_pdfs = module.has_pdfs
    db_module.has_websites = module.has_websites

    db.commit()
    db.refresh(db_module)
    return db_module
