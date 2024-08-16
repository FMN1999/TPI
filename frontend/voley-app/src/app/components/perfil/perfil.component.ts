import { Component, OnInit } from '@angular/core';
import { AuthService } from '../../services/auth/auth.service';
import { EstadisticasService } from '../../services/estadisticas/estadisticas.service';
import { NgIf } from "@angular/common";
import { FormsModule } from "@angular/forms";
import { ActivatedRoute } from '@angular/router';

@Component({
  selector: 'app-perfil',
  templateUrl: './perfil.component.html',
  standalone: true,
  imports: [
    NgIf,
    FormsModule
  ],
  styleUrls: ['./perfil.component.css']
})

export class PerfilComponent implements OnInit {
  perfil: any = {};
  esAsistente: boolean = false;
  mostrarFormulario: boolean = false;
  estadisticas: any = {};
  usuarioId: number = 1;
  selectedPartidoId = 0;

  constructor(
    private authService: AuthService,
    private estadisticasService: EstadisticasService,
    private route: ActivatedRoute
  ) {}

  ngOnInit(): void {
    this.route.params.subscribe(params => {
      const userId = params['id'];
      if (userId) {
        this.usuarioId = Number(userId);
      } else {
        const loggedInUserId = this.authService.getUsuarioId();
        if (loggedInUserId) {
          this.usuarioId = Number(loggedInUserId);
        } else {
          console.error('ID de usuario no encontrado');
        }
      }
      this.loadProfile();
      this.checkTipoUsuario();
      console.log(sessionStorage.getItem('tipoUsuario'))
      console.log(this.esAsistente)
    });
  }

  loadProfile(): void {
  this.authService.getProfileData(this.usuarioId).subscribe(
    data => {
      this.perfil = data;
      this.perfil.id_jugador = this.usuarioId;  // Asume que el perfil tiene este valor
      if (this.usuarioId !== Number(this.authService.getUsuarioId())) {
        this.perfil.id_asistente = Number(this.authService.getUsuarioId()); // Asigna el id_asistente del usuario logueado
      }
    },
    error => {
      console.error('Error al cargar el perfil:', error);
    }
  );
}

  checkTipoUsuario(): void {
    const tipoUsuario = sessionStorage.getItem('tipoUsuario');
    this.esAsistente = tipoUsuario === 'A';
  }

  onSubmit(): void {
    this.estadisticas.id_asistente = this.perfil.id_asistente;  // Asume que el perfil tiene este valor
    this.estadisticas.id_partido = this.selectedPartidoId;  // Debes tener una forma de seleccionar o asignar el partido
    this.estadisticas.id_jugador = this.perfil.id_jugador;  // Asume que el perfil tiene este valor
    this.estadisticasService.registrarEstadisticas(this.estadisticas).subscribe(
      response => {
        console.log('Estadísticas guardadas:', response);
        this.mostrarFormulario = false;
        this.estadisticas = {};
      },
      error => {
        console.error('Error al guardar las estadísticas:', error);
      }
    );
  }
}

