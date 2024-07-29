from typing import Optional, List
from database.connection import DataBase
from entities.models import Usuario


class UsuarioData(DataBase):
    def __init__(self):
        super().__init__()

    def GetAll(self) -> List[Usuario]:
        self.open()
        listaFamosos = list()
        try:
            self.cursor.execute("select * from Usuario", )
            for fam in self.cursor.fetchall():
                f = Usuario(*fam.values())
                listaFamosos.append(f)
            return listaFamosos

        except:
            print("Excepción ocurrida:")
            self.connection.rollback()
        finally:
            self.cursor.close()
            self.close()

    def GetOne(self, id) -> Optional[Usuario]:
        self.open()
        try:
            self.cursor.execute("SELECT * FROM Usuario WHERE id=%s", (id,))
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


if __name__ == '__main__':
    db = UsuarioData()
    db.GetOne(1)
