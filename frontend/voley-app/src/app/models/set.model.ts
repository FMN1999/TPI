import { Formacion } from "./formacion.model";

export interface Set {
  id: number;
  id_partido: number;
  puntos_local: number;
  puntos_visita: number;
  id_formacion_local: Formacion | undefined;
  id_formacion_visit: Formacion | undefined;
}
