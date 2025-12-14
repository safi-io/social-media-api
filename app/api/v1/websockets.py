from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, HTTPException
from sqlalchemy import and_, or_
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.chat_room import ChatRoom as chat_room_model
from app.models.message import Message as message_model
from app.models.user import User as user_model
from app.services.get_current_user import get_current_user, get_current_user_from_token
from app.websockets.manager import manager

router = APIRouter()


@router.websocket("/chat/{room_id}")
async def chat_ws(websocket: WebSocket, room_id: int):
    from app.db.session import get_db
    db = next(get_db())

    token = websocket.query_params.get("token")
    if not token:
        await websocket.close(code=1008)  # policy violation
        return
    current_user = get_current_user_from_token(db, token)
    if not current_user:
        await websocket.close(code=1008)
        return

    chat_room = db.query(chat_room_model).filter(chat_room_model.id == room_id).first()
    if not chat_room:
        await websocket.close(code=1008)  # chat room not found
        return

    if current_user.id not in [chat_room.user_one_id, chat_room.user_two_id]:
        await websocket.close(code=1008)  # user not in room
        return

    await websocket.accept()
    await manager.connect(room_id, websocket)

    try:
        while True:
            data = await websocket.receive_json()
            content = data.get("content")
            if not content:
                continue

            message = message_model(
                room_id=room_id,
                sender_id=current_user.id,
                content=content
            )
            db.add(message)
            db.commit()
            db.refresh(message)

            await manager.broadcast(
                room_id,
                {
                    "id": message.id,
                    "sender_id": message.sender_id,
                    "content": message.content,
                    "created_at": str(message.created_at)
                }
            )

    except WebSocketDisconnect:
        manager.disconnect(room_id, websocket)


@router.post("/chat-room/{user_id}")
def get_or_create_room(
        user_id: int,
        current_user=Depends(get_current_user),
        db: Session = Depends(get_db)
):
    if current_user.id == user_id:
        raise HTTPException(status_code=400, detail="You can't Create Room with Yourself.")

    # Verify the Second User Exists in DB

    other_user = db.query(user_model).filter(user_model.id == user_id).first()

    if not other_user:
        raise HTTPException(status_code=404, detail="Unable to Find the Next User.")

    room = db.query(chat_room_model).filter(
        or_(
            and_(chat_room_model.user_one_id == current_user.id,
                 chat_room_model.user_two_id == user_id),
            and_(chat_room_model.user_one_id == user_id,
                 chat_room_model.user_two_id == current_user.id),
        )
    ).first()

    if not room:
        room = chat_room_model(
            user_one_id=current_user.id,
            user_two_id=user_id
        )
        db.add(room)
        db.commit()
        db.refresh(room)

    return room
