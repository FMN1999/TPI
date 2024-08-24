import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class PosicionesService {
    private apiUrl = 'http://127.0.0.1:8000/api';

  constructor(private http: HttpClient) {}

  getPosicionesPorTemporada(temporadaId: string): Observable<any> {
    return this.http.get(`${this.apiUrl}/posiciones/${temporadaId}`);
  }

  agregarEquipoAlaTemporada(posicion: any): Observable<any> {
    return this.http.post(`${this.apiUrl}/posiciones/`, posicion);
  }

  eliminarPosicion(id: number): Observable<any> {
    return this.http.delete(`${this.apiUrl}/posicion/${id}/eliminar/`);
  }
}

