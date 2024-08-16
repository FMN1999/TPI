import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Equipo } from '../../models/equipo.model';
import {Jugador} from "../../models/user.model";

@Injectable({
  providedIn: 'root'
})
export class EquiposService {

  private baseUrl = 'http://127.0.0.1:8000/api';

  constructor(private http: HttpClient) {}

  getDts(): Observable<any[]> {
    return this.http.get<any[]>(`${this.baseUrl}/dts/`);
  }

  getAsistentes(): Observable<any[]> {
    return this.http.get<any[]>(`${this.baseUrl}/asistentes/`);
  }

  getJugadores(): Observable<any[]> {
    return this.http.get<any[]>(`${this.baseUrl}/jugadores/`);
  }

  crearEquipo(data: any): Observable<any> {
    return this.http.post(`${this.baseUrl}/crear-equipo/`, data);
  }

  getEquipos(): Observable<Equipo[]> {
    return this.http.get<Equipo[]>(`${this.baseUrl}/equipos/`);
  }

  getEquipo(id: number): Observable<Equipo> {
    return this.http.get<Equipo>(`${this.baseUrl}/equipos/${id}/`);
  }

  getJugadoresPorEquipo(id_equipo: number): Observable<Jugador[]> {
    return this.http.get<Jugador[]>(`${this.baseUrl}/equipos/${id_equipo}/jugadores/`);
  }
}
