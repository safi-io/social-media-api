from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from sqlalchemy import and_
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.project import Project as project_model
from app.models.project_member import ProjectMember as project_member_model
from app.schemas.project import Project, ProjectCreate, ProjectDelete
from app.services.get_current_user import get_current_user

router = APIRouter()


@router.post("/add-project", response_model=Project, summary="Creates a New Project and Assign Members.")
def create_project(new_project: ProjectCreate, current_user=Depends(get_current_user), db: Session = Depends(get_db)):
    new_project_data = new_project.model_dump()
    new_project_data["owner_id"] = current_user.id

    # Extract assigned members safely
    assigned_members = new_project_data.pop("assignments", None)

    try:
        # Create project
        created_project = project_model(**new_project_data)
        db.add(created_project)
        db.flush()

        # Assign members
        if assigned_members:
            for user_id, role in assigned_members.items():
                db.add(
                    project_member_model(
                        project_id=created_project.id,
                        user_id=int(user_id),
                        role=role
                    )
                )

        db.add(project_member_model(project_id=created_project.id, user_id=current_user.id, role="lead"))

        db.commit()
        db.refresh(created_project)

        return created_project

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Failed to create project: {str(e)}")


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
