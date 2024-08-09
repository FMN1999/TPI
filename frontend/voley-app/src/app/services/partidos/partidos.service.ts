import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

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
}
