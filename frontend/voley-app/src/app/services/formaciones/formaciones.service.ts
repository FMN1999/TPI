import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class FormacionService {

  private baseUrl = 'http://127.0.0.1:8000/api';

  constructor(private http: HttpClient) {}

  crearFormacion(data: any): Observable<any> {
    return this.http.post(`${this.baseUrl}/crear-formacion/`, data);
  }

  getFormacionesPorEquipo(id_equipo: number): Observable<any[]> {
    return this.http.get<any[]>(`${this.baseUrl}/equipos/${id_equipo}/formaciones/`);
  }
}

