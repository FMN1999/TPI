import { Component, OnInit } from '@angular/core';
import { AuthService } from '../../services/auth/auth.service';
import { EstadisticasService } from '../../services/estadisticas/estadisticas.service';
import {DecimalPipe, NgIf} from "@angular/common";
import { FormsModule } from "@angular/forms";
import { ActivatedRoute } from '@angular/router';
import {HeaderComponent} from "../header/header.component";

@Component({
  selector: 'app-perfil',
  templateUrl: './perfil.component.html',
  standalone: true,
  imports: [
    NgIf,
    FormsModule,
    DecimalPipe,
    HeaderComponent
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
  esJugador: boolean = false;
  esDt: boolean = false;
  editMode: boolean = false;
  perfilEditado: any = {};
  usuarioActual = 1;

  constructor(
    private authService: AuthService,
    private estadisticasService: EstadisticasService,
    private route: ActivatedRoute
  ) {}

  ngOnInit(): void {
    this.route.params.subscribe(params => {
      const userId = params['id'];
      this.usuarioActual = Number(this.authService.getUsuarioId());
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
    });
  }

  loadProfile(): void {
    this.authService.getProfileData(this.usuarioId).subscribe(
      data => {
        this.perfil = data;
        this.perfilEditado = { ...this.perfil };
        this.authService.obtenerTipoUsuario(this.perfil.id).subscribe(
          response => {
            this.esJugador = response.tipo === 'J';
            this.esDt = response.tipo === 'D';

            if (this.usuarioId !== Number(this.authService.getUsuarioId())) {
              this.perfil.id_asistente = Number(this.authService.getUsuarioId());
            }
            console.log(this.esJugador);

            if (this.esJugador) {
              this.loadEstadisticas();
            }
          },
          error => {
            console.error('Error al obtener el tipo de usuario:', error);
          }
        );
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

  loadEstadisticas(): void {
    this.estadisticasService.obtenerEstadisticasPorJugador(this.usuarioId).subscribe(
      data => {
        this.estadisticas = data;
      },
      error => {
        console.error('Error al cargar las estadísticas:', error);
      }
    );
  }

  onSubmit(): void {
    this.estadisticas.id_asistente = this.perfil.id_asistente;  // Asume que el perfil tiene este valor
    this.estadisticas.id_partido = this.selectedPartidoId;  // Debes tener una forma de seleccionar o asignar el partido
    this.estadisticas.id_jugador = this.perfil.id;  // Asume que el perfil tiene este valor
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
    this.loadEstadisticas()
  }

   // Habilitar modo de edición
  editProfile(): void {
    this.editMode = true;
  }

  // Guardar los cambios
  saveProfile(): void {
    this.authService.updateProfile(this.perfil.id, this.perfilEditado).subscribe(
      response => {
        console.log('Perfil actualizado:', response);
        this.perfil = { ...this.perfilEditado }; // Actualiza el perfil con los cambios guardados
        this.editMode = false; // Salir del modo de edición
      },
      error => {
        console.error('Error al actualizar el perfil:', error);
      }
    );
  }

  cancelEdit(): void {
    this.perfilEditado = { ...this.perfil }; // Revertir cambios
    this.editMode = false; // Salir del modo de edición
  }
}

