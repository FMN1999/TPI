import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class CambioService {

  private apiUrl = 'http://127.0.0.1:8000/api/registrar-cambio/';

  constructor(private http: HttpClient) { }

    registrarCambio(cambioData: any): Observable<any> {
      return this.http.post<any>(this.apiUrl, cambioData);
    }
}

