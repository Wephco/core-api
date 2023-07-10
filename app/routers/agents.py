from fastapi import status, HTTPException, Depends, APIRouter, Response
from sqlalchemy.orm import Session
from ..db.database import get_db
from ..db.database_models import Agent, User
from ..schemas.agents import AgentBase, AgentResponse
from ..auth.oauth import get_current_user
from typing import List
from ..utils.enums import Roles


router = APIRouter(
    prefix="/api/agents",
    tags=["Agents"]
)


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=AgentResponse)
async def create_agent(agent: AgentBase, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):

    if current_user.role not in (Roles.admin, Roles.super_admin, Roles.staff, Roles.support):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail='Not Authorized')

    new_agent = Agent(**agent.dict())
    db.add(new_agent)
    db.commit()
    db.refresh(new_agent)

    return new_agent


@router.get('/', response_model=List[AgentResponse])
async def get_agents(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):

    if current_user.role not in (Roles.admin, Roles.super_admin, Roles.staff, Roles.support):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail='Not Authorized')

    agents = db.query(Agent).all()

    return agents


@router.get('/{id}', response_model=AgentResponse)
async def get_agent(id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):

    if current_user.role not in (Roles.admin, Roles.super_admin, Roles.staff, Roles.support):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail='Not Authorized')

    agent = db.query(Agent).filter(Agent.id == id).first()

    if not agent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Agent not found')

    return agent


@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED, response_model=AgentResponse)
async def update_agent(id: int, agent: AgentBase, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):

    if current_user.role not in (Roles.admin, Roles.super_admin, Roles.staff):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail='Not Authorized')

    agent_query = db.query(Agent).filter(Agent.id == id)

    if not agent_query.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Agent not found')

    agent_query.update(agent.dict(), synchronize_session=False)
    db.commit()
    db.refresh(agent_query.first())

    updated_agent = agent_query.first()

    return updated_agent


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_agent(id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):

    if current_user.role not in (Roles.admin, Roles.super_admin):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail='Not Authorized')

    agent = db.query(Agent).filter(Agent.id == id)

    if not agent.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Agent not found')

    agent.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)
