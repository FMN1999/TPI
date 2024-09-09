import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class EstadisticasService {
  private apiUrl = 'https://tpi-voley-ff1849e1408c.herokuapp.com/api'; // Asegúrate de que esta URL sea correcta

  constructor(private http: HttpClient) { }

  registrarEstadisticas(estadisticas: any): Observable<any> {
    return this.http.post(`${this.apiUrl}/estadisticas/`, estadisticas);
  }

  obtenerEstadisticasPorJugador(id_jugador: number): Observable<any> {
    return this.http.get(`${this.apiUrl}/estadisticas/jugador/${id_jugador}/`);
  }
}

