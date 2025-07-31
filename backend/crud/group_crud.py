from sqlalchemy.orm import Session
from backend.models.group import Group, GroupMember
from backend.schemas.group_schema import GroupCreate, GroupUpdate
from backend.models.user import User
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError


class GroupCRUD:
    def __init__(self, db: Session):
        self.db = db

    # --- GROUP CRUD ---
    def create_group(self, group_data: GroupCreate) -> Group:
        group = Group(**group_data.dict())
        self.db.add(group)
        self.db.commit()
        self.db.refresh(group)
        return group

    def get_group_by_id(self, group_id: int) -> Group | None:
        return self.db.query(Group).filter(Group.id == group_id).first()

    def get_all_groups(self) -> list[Group]:
        return self.db.query(Group).all()

    def update_group(self, group_id: int, updates: GroupUpdate) -> Group | None:
        group = self.get_group_by_id(group_id)
        if not group:
            return None
        for key, value in updates.dict(exclude_unset=True).items():
            setattr(group, key, value)
        self.db.commit()
        self.db.refresh(group)
        return group

    def delete_group(self, group_id: int) -> bool:
        group = self.get_group_by_id(group_id)
        if not group:
            return False
        self.db.delete(group)
        self.db.commit()
        return True

    # --- GROUP MEMBERSHIP ---

    def add_user_to_group(self, group_id: int, user_id: int) -> GroupMember:
        # Ensure group and user exist
        if not self.db.query(Group).filter_by(id=group_id).first():
            raise HTTPException(status_code=404, detail="Group not found")
        if not self.db.query(User).filter_by(id=user_id).first():
            raise HTTPException(status_code=404, detail="User not found")

        new_member = GroupMember(group_id=group_id, user_id=user_id)
        self.db.add(new_member)
        try:
            self.db.commit()
        except IntegrityError:
            self.db.rollback()
            raise HTTPException(status_code=400, detail="User already in group")

        self.db.refresh(new_member)
        return new_member

    def remove_user_from_group(self, group_id: int, user_id: int) -> bool:
        membership = (
            self.db.query(GroupMember)
            .filter_by(group_id=group_id, user_id=user_id)
            .first()
        )
        if not membership:
            return False

        self.db.delete(membership)
        self.db.commit()
        return True

    def get_group_members(self, group_id: int) -> list[User]:
        group = self.get_group_by_id(group_id)
        if not group:
            raise HTTPException(status_code=404, detail="Group not found")
        return group.members
