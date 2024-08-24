export interface Equipo {
  id: number;
  nombre: string;
  logo: string;
  direccion: string;
  ciudad: string;
  provincia: string;
  cant_victorias_local: number;
  cant_victorias_visit: number;
  campeonatos: number;
  campeones_actuales: boolean;
  dts: Array<{ id: number; nombre: string; apellido: string }>;
  asistentes: Array<{ id: number; nombre: string; apellido: string }>;
  jugadores: Array<{ id: number; nombre: string; apellido: string; nro_jugador: number; posicion_pcpal: string }>;
}

