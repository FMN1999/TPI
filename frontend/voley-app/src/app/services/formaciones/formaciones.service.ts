import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class FormacionService {

  private baseUrl = 'https://tpi-voley-ff1849e1408c.herokuapp.com/api';

  constructor(private http: HttpClient) {}

  crearFormacion(data: any): Observable<any> {
    return this.http.post(`${this.baseUrl}/crear-formacion/`, data);
  }

  getFormacionesPorEquipo(id_equipo: number): Observable<any[]> {
    return this.http.get<any[]>(`${this.baseUrl}/obtener-formaciones/${id_equipo}/`);
  }

  eliminarFormacion(id: number): Observable<any> {
      return this.http.delete(`${this.baseUrl}/formaciones/${id}/`);
    }
}

