import { Component, AfterViewInit } from '@angular/core';
import { AuthService } from '../../services/auth/auth.service';
import { EstadisticasService } from '../../services/estadisticas/estadisticas.service';
import { DecimalPipe, NgIf } from "@angular/common";
import { FormsModule } from "@angular/forms";
import { ActivatedRoute } from '@angular/router';
import { HeaderComponent } from "../header/header.component";
import { Chart, registerables } from 'chart.js';

Chart.register(...registerables);

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
export class PerfilComponent implements AfterViewInit {
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

  ngAfterViewInit(): void {
    if (this.esJugador) {
      this.createRadarChart();
    }
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
        this.createRadarChart(); // Mueve la llamada aquí
      },
      error => {
        console.error('Error al cargar las estadísticas:', error);
      }
    );
  }

  onSubmit(): void {
    this.estadisticas.id_asistente = this.perfil.id_asistente;
    this.estadisticas.id_partido = this.selectedPartidoId;
    this.estadisticas.id_jugador = this.perfil.id;
    this.estadisticasService.registrarEstadisticas(this.estadisticas).subscribe(
      response => {
        this.mostrarFormulario = false;
        this.estadisticas = {};
      },
      error => {
        console.error('Error al guardar las estadísticas:', error);
      }
    );
    this.loadEstadisticas();
  }

  editProfile(): void {
    this.editMode = true;
  }

  saveProfile(): void {
    this.authService.updateProfile(this.perfil.id, this.perfilEditado).subscribe(
      response => {
        console.log('Perfil actualizado:', response);
        this.perfil = { ...this.perfilEditado };
        this.editMode = false;
      },
      error => {
        console.error('Error al actualizar el perfil:', error);
      }
    );
  }

  cancelEdit(): void {
    this.perfilEditado = { ...this.perfil };
    this.editMode = false;
  }

  createRadarChart() {
    const ctx = document.getElementById('estadisticasRadar') as HTMLCanvasElement;

    if (ctx) {
      new Chart(ctx, {
        type: 'radar',
        data: {
          labels: [
            'Remates',
            'Bloqueos',
            'Saques',
            'Defensas',
            'Recepciones'
          ],
          datasets: [{
            label: 'Porcentaje de Aciertos',
            data: [
              this.estadisticas.porcentaje_aciertos_remates,
              this.estadisticas.porcentaje_aciertos_bloqueos,
              this.estadisticas.porcentaje_aciertos_saques,
              this.estadisticas.porcentaje_aciertos_defensas,
              this.estadisticas.porcentaje_aciertos_recepciones
            ],
            fill: true,
            backgroundColor: 'rgba(0, 123, 255, 0.5)',
            borderColor: 'rgba(0, 123, 255, 1)',
            pointBackgroundColor: 'rgba(0, 123, 255, 1)',
            pointBorderColor: '#fff',
            pointHoverBackgroundColor: '#fff',
            pointHoverBorderColor: 'rgba(0, 123, 255, 1)'
          }]
        },
        options: {
          scales: {
            r: {
              angleLines: {
                display: true
              },
              suggestedMin: 0,
              suggestedMax: 100
            }
          },
          plugins: {
            legend: {
              display: false
            }
          }
        }
      });
    } else {
      console.error('Canvas element not found');
    }
  }
}


