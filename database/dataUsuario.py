from typing import Optional
from database.connection import DataBase
from entities.models import Usuario


class UsuarioData(DataBase):
    def __init__(self):
        super().__init__()

    def GetOne(self, usuario) -> Optional[Usuario]:
        self.open()
        try:
            self.cursor.execute("SELECT * FROM Usuario WHERE usuario=%s", (usuario,))
            result = self.cursor.fetchone()
            if result:
                u = Usuario(*result.values())
                return u
            else:
                return None
        except Exception as e:
            print(f"No se pudo encontrar al usuario: {e}")
            self.connection.rollback()
            return None
        finally:
            self.close()