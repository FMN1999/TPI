import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { tap } from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private apiUrl = 'https://tpi-voley-ff1849e1408c.herokuapp.com/api';
  private tipoUsuario = '';

  constructor(private http: HttpClient) {}

  login(username: string, password: string): Observable<any> {
    return this.http.post(`${this.apiUrl}/login/`, { usuario: username, contrasenia: password }).pipe(
      tap((response: any) => {
        if (typeof window !== 'undefined' && response.user_id) {
          sessionStorage.setItem('user_id', response.user_id); // Guardamos el ID de usuario
        } else {
          console.error('user_id no encontrado en la respuesta del login');
        }
      })
    );
  }

  register(userData: any): Observable<any> {
    return this.http.post(`${this.apiUrl}/register/`, userData);
  }

  logout(): void {
    if (typeof window !== 'undefined') {
      sessionStorage.removeItem('user_id'); // Quitamos el ID de usuario
    }
  }

  isAuthenticated(): boolean {
    if (typeof window !== 'undefined') {
      return !!sessionStorage.getItem('user_id');
    }
    return false;
  }

  getUsuarioId(): string | null {
    if (typeof window !== 'undefined') {
      return sessionStorage.getItem('user_id');
    }
    return null;
  }

  getProfileData(usuarioId: number): Observable<any> {
    return this.http.get(`${this.apiUrl}/usuario/${usuarioId}/`);
  }

  obtenerTipoUsuario(idUsuario: number): Observable<any> {
    return this.http.get<any>(`${this.apiUrl}/usuario/${idUsuario}/tipo/`);
  }

  guardarTipoUsuario(tipo: string): void {
    this.tipoUsuario = tipo;
    // Almacena la inicial en el local storage o en una variable global según tu preferencia
    sessionStorage.setItem('tipoUsuario', tipo);
  }

  updateProfile(usuarioId: number, perfilEditado: any): Observable<any> {
    return this.http.put(`${this.apiUrl}/usuarios/${usuarioId}/`, perfilEditado);
  }
}


