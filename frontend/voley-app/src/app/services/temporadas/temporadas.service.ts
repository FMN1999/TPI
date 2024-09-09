import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class TemporadaService {

  private baseUrl = 'https://tpi-voley-ff1849e1408c.herokuapp.com/api';

  constructor(private http: HttpClient) { }

  getTemporadasPorLiga(ligaId: string | null): Observable<any> {
    return this.http.get(`${this.baseUrl}/liga/${ligaId}/temporadas/`);
  }

  crearTemporada(temporada: any): Observable<any> {
    return this.http.post(`${this.baseUrl}/temporada/crear/`, temporada);
  }

  getTemporada(id: string): Observable<any> {
    return this.http.get(`${this.baseUrl}/temporada/${id}`);
  }

  eliminarTemporada(id: number): Observable<any> {
    return this.http.delete(`${this.baseUrl}/temporada/${id}/eliminar/`);
  }
}
