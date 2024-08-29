import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import {Partido} from "../../models/partido.model";

@Injectable({
  providedIn: 'root'
})
export class PartidoService {

  private baseUrl = 'http://127.0.0.1:8000/api';

  constructor(private http: HttpClient) {}

  agregarPartido(partido: any): Observable<any> {
    return this.http.post(`${this.baseUrl}/partido/`, partido);
  }

  getPartidosPorTemporada(temporadaId: string): Observable<any> {
    return this.http.get(`${this.baseUrl}/partido/${temporadaId}/`);
  }

  getPartidosSinSetsGanados(): Observable<Partido[]> {
    return this.http.get<Partido[]>(`${this.baseUrl}/partidos-sin-sets-ganados/`);
  }

  getDetallesPartido(id: number): Observable<any> {
    return this.http.get(`${this.baseUrl}/partido-vista/${id}/`);
  }

  agregarSet(data: any): Observable<any> {
    return this.http.post(`${this.baseUrl}/partido/agregar-set/`, data);
  }

  terminarPartido(idPartido: number): Observable<any> {
    const formData = new FormData();
    formData.append('id_partido', idPartido.toString());
    return this.http.post(`${this.baseUrl}/partido/terminar/`, formData);
  }

  obtenerFormaciones(idEquipo: number): Observable<any> {
    return this.http.get(`${this.baseUrl}/obtener-formaciones/${idEquipo}/`);
  }

  // Obtener los sets de un partido
  obtenerSets(idPartido: number): Observable<any> {
    return this.http.get(`${this.baseUrl}/obtener-sets/${idPartido}/`);
  }

  eliminarPartido(partidoId: number): Observable<any> {
    return this.http.delete(`${this.baseUrl}/eliminar-partido/${partidoId}/`);
  }

  eliminarSet(idSet: number): Observable<any> {
    return this.http.delete(`${this.baseUrl}/sets/eliminar/${idSet}/`);
  }
}
