import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class UsuariosService {
  private apiUrl = 'https://tpi-voley-ff1849e1408c.herokuapp.com/api'; // Asegúrate de que esta URL sea correcta

  constructor(private http: HttpClient) { }

  obtenerUsuarios(): Observable<any[]> {
    return this.http.get<any[]>(`${this.apiUrl}/usuarios/`);
  }
}
