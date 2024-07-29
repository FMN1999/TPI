from typing import List
from database.dataUsuario import UsuarioData
from entities.models import Usuario


class UsuarioController:
    usuario_data = UsuarioData()

    def GetUsuarios(self) -> List[Usuario]:
        return self.usuario_data.GetAll()

    def GetUsuario(self, id: int) -> Usuario:
        return self.usuario_data.GetOne(id)