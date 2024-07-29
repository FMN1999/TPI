import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';
import {FormsModule} from "@angular/forms";
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
    tipo_usuario: '',
    telefono: '',  // Solo para DT
    altura: null,  // Solo para Jugador
    peso: null     // Solo para Jugador
  };

  constructor(private http: HttpClient, private router: Router) {}

  onSubmit() {
    const userData = {
      ...this.registroData,
      telefono: this.registroData.tipo_usuario === 'DT' ? this.registroData.telefono : null,
      altura: this.registroData.tipo_usuario === 'Jugador' ? this.registroData.altura : null,
      peso: this.registroData.tipo_usuario === 'Jugador' ? this.registroData.peso : null
    };

    this.http.post('http://127.0.0.1:8000/api/register/', userData).subscribe(
      (response: any) => {
        console.log('Registro exitoso', response);
        this.router.navigate(['/login']).then(r =>{} );
      },
      (error) => {
        console.error('Error en el registro', error);
      }
    );
  }

  onTipoUsuarioChange(event: any) {
    this.registroData.tipo_usuario = event.target.value;
  }
}

