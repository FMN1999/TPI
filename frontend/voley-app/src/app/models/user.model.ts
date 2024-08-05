export interface Usuario {
  id: number;
  nombre: string;
  apellido: string;
}

export interface Jugador extends Usuario {
  altura: number;
  peso: number;
}

export interface Asistente extends Usuario {}

export interface DT extends Usuario {
  telefono: string;
}
