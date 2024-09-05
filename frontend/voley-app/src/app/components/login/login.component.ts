import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { AuthService } from '../../services/auth/auth.service';
import { HttpClientModule } from '@angular/common/http';
import { NgIf } from '@angular/common'

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  standalone: true,
  styleUrls: ['./login.component.css'],
  imports: [FormsModule, HttpClientModule, NgIf]
})
export class LoginComponent {
  username: string = '';
  password: string = '';
  errorMessage: string = '';  // Variable para manejar errores

  constructor(private authService: AuthService, private router: Router) {}

  ngOnInit(): void {
    // Verificar si el usuario ya está autenticado
    const userId = sessionStorage.getItem('user_id');

    if (userId) {
      // Redirigir al usuario al home si ya está autenticado
      this.router.navigate(['/']).then(r => {});
    }
  }

  onSubmit(): void {
    // Verificar si ambos campos están completos
    if (!this.username || !this.password) {
      this.errorMessage = 'Por favor, complete ambos campos';  // Mensaje de error si falta algún campo
      return;
    }

    this.authService.login(this.username, this.password).subscribe(
      response => {
        localStorage.setItem('token', response.token);

        const idUsuario = sessionStorage.getItem('user_id'); // Obtenemos el ID del usuario de la sesión
        if (idUsuario) {
          const idUsuarioNumber = Number(idUsuario); // Convertimos a número
          this.authService.obtenerTipoUsuario(idUsuarioNumber).subscribe(
            (response) => {
              this.authService.guardarTipoUsuario(response.tipo);
              this.router.navigate(['/']).then(r=>{});
            },
            (error) => {
              console.error('Error al obtener el tipo de usuario:', error);
            }
          );
        } else {
          this.errorMessage = 'ID de usuario no encontrado en la respuesta del login';
        }
      },
      error => {
          this.errorMessage = 'Nombre de usuario o contraseña incorrectos';
      }
    );
  }

  cerrarFormulario(): void {
    this.router.navigate(['/']).then(r => {});
  }

  irARegistro(): void {
    this.router.navigate(['/register']).then(r => {});
  }
}





