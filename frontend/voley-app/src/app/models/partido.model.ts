import {Set} from './set.model';

export interface Partido {
  id: number;
  local: string;
  visita: string;
  set_ganados_local: number;
  set_ganados_visita: number;
  sets: Set[]; // Relación con los sets del partido
  fecha: string; // O Date si prefieres usar objetos Date en lugar de cadenas
  id_local: number; // ID del equipo local
  id_visita: number; // ID del equipo visitante
  estado: string;
  logo_local: string;
  logo_visita: string;
  hora:string;
}
