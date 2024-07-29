import { Component, OnInit } from '@angular/core';
import { AuthService } from '../../services/auth/auth.service';

@Component({
  selector: 'app-perfil',
  templateUrl: './perfil.component.html',
  styleUrls: ['./perfil.component.css']
})
export class PerfilComponent implements OnInit {
  perfil: any = {};
  usuarioId: number = 1; // Cambia esto al ID del usuario logueado; normalmente obtendrás esto del token o de la autenticación

  constructor(private authService: AuthService) {}

  ngOnInit(): void {
    this.loadProfile();
  }

  loadProfile(): void {
    this.authService.getProfileData(this.usuarioId).subscribe(
      data => {
        this.perfil = data;
      },
      error => {
        console.error('Error al cargar el perfil:', error);
      }
    );
  }
}
