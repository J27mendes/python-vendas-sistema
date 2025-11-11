from typing import Optional
from abc import ABC, abstractmethod

class BaseModel(ABC):
    """
    Classe base abstrata para todas as entidades de domínio.
    
    """
    
    def __init__(self, id: Optional[int] = None):
        # Herança: O atributo 'id' é definido e herdado
        self.id = id

    @abstractmethod
    def __repr__(self):
        """
        2. Polimorfismo: Obriga todas as classes filhas a definirem
        sua própria representação de string (sobrescrita).
        """
        pass