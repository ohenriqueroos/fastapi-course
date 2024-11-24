from decimal import *
from typing import List

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from shared.dependencies import get_db

from contas_a_pagar_e_receber.models.conta_a_pagar_receber_model import ContaPagarReceber

router = APIRouter(prefix="/contas-a-pagar-e-receber")


class ContaPagarReceberResponse(BaseModel):
    id: int
    descricao: str
    valor: Decimal
    tipo: str  # PAGAR, RECEBER


class ContaPagarReceberRequest(BaseModel):
    descricao: str
    valor: Decimal
    tipo: str  # PAGAR, RECEBER

class Config:
    orm_mode = True


@router.get("", response_model=List[ContaPagarReceberResponse])
def listar_contas(db: Session = Depends(get_db)) -> List[ContaPagarReceberResponse]:
    return db.query(ContaPagarReceber).all()

@router.post("", response_model=ContaPagarReceberResponse, status_code=201)
def criar_conta(conta_a_pagar_e_receber_request: ContaPagarReceberRequest, db: Session = Depends(get_db)) -> ContaPagarReceberResponse:
    contas_a_pagar_e_receber = ContaPagarReceber(
        **conta_a_pagar_e_receber_request.model_dump()
    )

    db.add(contas_a_pagar_e_receber)
    db.commit()
    db.refresh(contas_a_pagar_e_receber)

    return contas_a_pagar_e_receber