import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { AuthService } from '../../services/auth/auth.service';
import { HttpClientModule } from '@angular/common/http';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  standalone: true,
  styleUrls: ['./login.component.css'],
  imports: [FormsModule, HttpClientModule]
})
export class LoginComponent {
  username: string = '';
  password: string = '';

  constructor(private authService: AuthService, private router: Router) {}

  onSubmit(): void {
    this.authService.login(this.username, this.password).subscribe(
      response => {
        localStorage.setItem('token', response.token);

        const idUsuario = sessionStorage.getItem('user_id'); // Obtenemos el ID del usuario de la sesión
        if (idUsuario) {
          const idUsuarioNumber = Number(idUsuario); // Convertimos a número
          this.authService.obtenerTipoUsuario(idUsuarioNumber).subscribe(
            (response) => {
              this.authService.guardarTipoUsuario(response.tipo);
              this.router.navigate(['/']).then(r => {});
            },
            (error) => {
              console.error('Error al obtener el tipo de usuario:', error);
            }
          );
        } else {
          console.error('ID de usuario no encontrado en la respuesta del login');
        }
      },
      error => {
        console.error('Login error', error);
      }
    );
  }


}



