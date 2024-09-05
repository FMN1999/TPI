import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';
import {FormsModule, NgForm} from "@angular/forms";
import {NgIf} from "@angular/common";

@Component({
  selector: 'app-register',
  templateUrl: './register.component.html',
  standalone: true,
  imports: [
    FormsModule,
    NgIf
  ],
  styleUrls: ['./register.component.css']
})
export class RegisterComponent {
  registroData = {
    usuario: '',
    contrasenia: '',
    email: '',
    nombre: '',
    apellido: '',
    sexo: '',
    fecha_nacimiento: '',
    ciudad_nacimiento: '',
    provincia_nacimiento: '',
    tipo_usuario: '',
    telefono: '',  // Solo para DT
    altura: null,  // Solo para Jugador
    peso: null     // Solo para Jugador
  };
  errorMessage: string = '';

  constructor(private http: HttpClient, private router: Router) {}

  ngOnInit(): void {
    // Verificar si el usuario ya está autenticado
    const userId = sessionStorage.getItem('user_id')

    if (userId) {
      // Redirigir al usuario al home si ya está autenticado
      this.router.navigate(['/']).then(r => {});
    }
  }

  onSubmit(form: NgForm) {
    if (form.invalid) {
      this.errorMessage = 'Por favor complete todos los campos requeridos.';
      return;
    }

    const userData = {
      ...this.registroData,
      telefono: this.registroData.tipo_usuario === 'DT' ? this.registroData.telefono : null,
      altura: this.registroData.tipo_usuario === 'Jugador' ? this.registroData.altura : null,
      peso: this.registroData.tipo_usuario === 'Jugador' ? this.registroData.peso : null
    };

    this.http.post('http://127.0.0.1:8000/api/register/', userData).subscribe(
      (response: any) => {
        this.router.navigate(['/login']).then(r => {} );
      },
      (error) => {
        this.errorMessage = error.error?.error || 'El usuario o email ya existe. Intente nuevamente con uno nuevo.';
      }
    );
  }

  onTipoUsuarioChange(event: any) {
    this.registroData.tipo_usuario = event.target.value;
  }
}

