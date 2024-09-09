import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class CambioService {

  private apiUrl = 'https://tpi-voley-ff1849e1408c.herokuapp.com/api';

  constructor(private http: HttpClient) { }

    registrarCambio(cambioData: any): Observable<any> {
      return this.http.post<any>(`${this.apiUrl}/registrar-cambio/`, cambioData);
    }

    obtenerCambiosPorPartido(idPartido: number): Observable<any[]> {
    return this.http.get<any[]>(`${this.apiUrl}/cambios/partido/${idPartido}/`);
  }
}

