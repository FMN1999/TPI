import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable} from 'rxjs';
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

  crearEquipo(equipoData: any): Observable<any> {
    return this.http.post(`${this.baseUrl}/crear-equipo/`, equipoData);
  }

  getEquipos(): Observable<Equipo[]> {
    return this.http.get<Equipo[]>(`${this.baseUrl}/equipos/`);
  }

  getEquipo(id: number): Observable<Equipo> {
    return this.http.get<Equipo>(`${this.baseUrl}/equipos/${id}/`);
  }

  getJugadoresPorEquipo(id_equipo: number): Observable<any[]> {
    return this.http.get<any[]>(`${this.baseUrl}/equipos/${id_equipo}/jugadores/`);
  }

  darDeBajaMiembro(tipo: string, miembroId: number): Observable<any> {
    return this.http.post(`${this.baseUrl}/equipos/baja/${tipo}/${miembroId}/`, {});
  }

  getDtsLibres(): Observable<any[]> {
    return this.http.get<any[]>(`${this.baseUrl}/dts/`);
  }

  // Obtener Asistentes libres
  getAsistentesLibres(): Observable<any[]> {
    return this.http.get<any[]>(`${this.baseUrl}/asistentes/`);
  }

  // Obtener Jugadores libres
  getJugadoresLibres(): Observable<Jugador[]> {
    return this.http.get<Jugador[]>(`${this.baseUrl}/jugadores/`);
  }
  // Agregar DT a equipo
  agregarDt(idEquipo: number, idDt: number): Observable<any> {
    return this.http.post(`${this.baseUrl}/equipos/${idEquipo}/agregar/dt/${idDt}/`, {});
  }

  // Agregar Asistente a equipo
  agregarAsistente(idEquipo: number, idAsistente: number): Observable<any> {
    return this.http.post(`${this.baseUrl}/equipos/${idEquipo}/agregar/asistente/${idAsistente}/`, {});
  }

  // Agregar Jugador a equipo
  agregarJugador(idEquipo: number, idJugador: number, jugadorData: any): Observable<any> {
    return this.http.post(`${this.baseUrl}/equipos/${idEquipo}/agregar/jugador/${idJugador}/`, jugadorData);
  }

  verificarAsistente(idEquipo: number, idUsuario: number): Observable<{ es_asistente: boolean }> {
    return this.http.get<{ es_asistente: boolean }>(`${this.baseUrl}/equipos/${idEquipo}/verificar-asistente/${idUsuario}/`);
  }

  verificarDt(idEquipo: number, idUsuario: number): Observable<{ es_dt: boolean }> {
    return this.http.get<{ es_dt: boolean }>(`${this.baseUrl}/equipos/${idEquipo}/verificar-dt/${idUsuario}/`);
  }

  getEquiposTemporada(idTemporada:number):Observable<Equipo[]>{
    return this.http.get<Equipo[]>(`${this.baseUrl}/equipos-temporada/${idTemporada}/`);
  }
}
