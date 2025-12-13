import json

from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from fastapi.params import Depends
from sqlalchemy import and_
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.project import Project as project_model
from app.models.project_member import ProjectMember as project_member_model
from app.schemas.project import Project, ProjectCreate, ProjectDelete
from app.services.cloudinary import upload_image
from app.services.get_current_user import get_current_user

router = APIRouter()


@router.post("/add-project", response_model=Project)
def create_project(
        new_project: str = Form(...),
        media: list[UploadFile] | None = File(None),
        current_user=Depends(get_current_user),
        db: Session = Depends(get_db),
):
    try:
        project_data = ProjectCreate(**json.loads(new_project))
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid project data")

    new_project_data = project_data.model_dump()
    new_project_data["owner_id"] = current_user.id

    assigned_members = new_project_data.pop("assignments", None)

    created_project = project_model(**new_project_data)
    db.add(created_project)
    db.flush()

    if assigned_members:
        for user_id, role in assigned_members.items():
            db.add(project_member_model(
                project_id=created_project.id,
                user_id=int(user_id),
                role=role
            ))

    db.add(project_member_model(
        project_id=created_project.id,
        user_id=current_user.id,
        role="lead"
    ))

    if media:
        cloudinary_folder = f"projects/{created_project.id}"

        for file in media:
            file.file.seek(0, 2)
            file_size = file.file.tell()
            file.file.seek(0)

            if file_size > 0:
                upload_image(file, cloudinary_folder)
            else:
                print(f"Skipping empty file: {file.filename}")

        created_project.external_urls = {
            "cloudinary_folder": cloudinary_folder
        }
    else:
        created_project.external_urls = {}

    db.commit()
    db.refresh(created_project)

    members = db.query(project_member_model).filter(project_member_model.project_id == created_project.id).all()
    assignments = {str(member.user_id): member.role for member in members}

    created_project.assignments = assignments

    return created_project


@router.post("/remove-project")
def delete_project(data: ProjectDelete,
                   current_user=Depends(get_current_user),
                   db: Session = Depends(get_db)):
    current_user_id = current_user.id
    project_to_delete = db.query(project_model).filter(
        and_(
            project_model.id == data.project_id,
            project_model.owner_id == current_user_id
        ))

    if not project_to_delete:
        raise HTTPException(status_code=404, detail="You can't Delete this Project.")

    deleted = project_to_delete.delete()

    if deleted == 0:
        raise HTTPException(status_code=500, detail="Unable to Delete this Project.")

    db.commit()

    return {"message": "Deleted Successfully."}


@router.get("/my-projects", response_model=list[Project])
def my_projects(current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    project_ids = [pid[0] for pid in db.query(project_member_model.project_id)
    .filter(project_member_model.user_id == current_user.id)
    .all()]

    projects = db.query(project_model).filter(project_model.id.in_(project_ids)).all()

    result = []
    for project in projects:
        members = db.query(project_member_model).filter(project_member_model.project_id == project.id).all()
        assignments = {str(member.user_id): member.role for member in members}

        proj_data = Project.from_orm(project).dict()
        proj_data["assignments"] = assignments
        result.append(proj_data)

    return result
