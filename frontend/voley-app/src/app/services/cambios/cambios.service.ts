import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class CambioService {

  private apiUrl = 'http://127.0.0.1:8000/api';

  constructor(private http: HttpClient) { }

    registrarCambio(cambioData: any): Observable<any> {
      return this.http.post<any>(`${this.apiUrl}/registrar-cambio/`, cambioData);
    }

    obtenerCambiosPorPartido(idPartido: number): Observable<any[]> {
    return this.http.get<any[]>(`${this.apiUrl}/cambios/partido/${idPartido}/`);
  }
}

