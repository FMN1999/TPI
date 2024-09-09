import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class LigaService {
  private apiUrl = 'https://tpi-voley-ff1849e1408c.herokuapp.com/api'; // Ajusta la URL según sea necesario

  constructor(private http: HttpClient) {}

  crearLiga(liga: any): Observable<any> {
    return this.http.post(`${this.apiUrl}/crear-liga/`, liga);
  }

  obtenerLigas(): Observable<any[]> {
    return this.http.get<any[]>(`${this.apiUrl}/ligas/`);
  }

  obtenerLigaPorId(id: string | null): Observable<any> {
    return this.http.get<any>(`${this.apiUrl}/ligas/${id}/`);
  }
}
