import { Component, OnInit } from '@angular/core';
import { EquiposService } from '../../services/equipos/equipos.service';
import { AuthService } from '../../services/auth/auth.service';
import { FormsModule, ReactiveFormsModule } from "@angular/forms";
import { NgForOf, NgIf } from "@angular/common";
import { Router } from '@angular/router';

@Component({
  selector: 'app-alta-equipo',
  templateUrl: './alta-equipo.component.html',
  standalone: true,
  imports: [
    ReactiveFormsModule,
    NgForOf,
    NgIf,
    FormsModule
  ],
  styleUrls: ['./alta-equipo.component.css']
})
export class AltaEquipoComponent implements OnInit {
  dts: any[] = [];
  asistentes: any[] = [];
  jugadores: any[] = [];
  selectedDt: any = null;
  selectedAsistentes: any[] = [];
  selectedJugadores: any[] = [];
  team: any = {
    nombre: '',
    logo: '',
    direccion: '',
    ciudad: '',
    provincia: '',
    cant_victorias_local: 0,
    cant_victorias_visit: 0,
    campeonatos: 0,
    campeones_actuales: false
  };
  errorMessage: string = '';
  tipo: string | undefined;

  constructor(private equiposService: EquiposService, private router: Router, private authService: AuthService) {}

  ngOnInit(): void {
    this.getDts();
    this.getAsistentes();
    this.getJugadores();
    const idUsuario= this.authService.getUsuarioId();

    this.authService.obtenerTipoUsuario(Number(idUsuario)).subscribe((data: { tipo: string; }) => {
      this.tipo = data.tipo;
    });
  }

  getDts(): void {
    this.equiposService.getDts().subscribe(data => {
      this.dts = data;
    });
  }

  getAsistentes(): void {
    this.equiposService.getAsistentes().subscribe(data => {
      this.asistentes = data;
    });
  }

  getJugadores(): void {
    this.equiposService.getJugadores().subscribe(data => {
      this.jugadores = data;
    });
  }

  onDtChange(event: Event): void {
    const selectElement = event.target as HTMLSelectElement;
    const dtId = +selectElement.value;
    this.selectedDt = this.dts.find(dt => dt.id === dtId) || { id: dtId, fecha_desde: '', fecha_hasta: '' };
  }

  onAsistentesChange(event: Event): void {
    const selectElement = event.target as HTMLSelectElement;
    this.selectedAsistentes = Array.from(selectElement.selectedOptions)
      .map(option => {
        const id = +option.value;
        return this.asistentes.find(asistente => asistente.id === id) || { id, fecha_desde: '', fecha_hasta: '' };
      });

    // Limitar a 4 asistentes
    if (this.selectedAsistentes.length > 4) {
      this.selectedAsistentes = this.selectedAsistentes.slice(0, 4);
    }
  }

  onJugadoresChange(event: Event): void {
    const selectElement = event.target as HTMLSelectElement;
    this.selectedJugadores = Array.from(selectElement.selectedOptions)
      .map(option => {
        const id = +option.value;
        return this.jugadores.find(jugador => jugador.id === id) || { id, nro_jugador: '', posicion_pcpal: '', posicion_secundaria: '', fecha_ingreso: '', fecha_salida: '' };
      });

    // Limitar a 20 jugadores
    if (this.selectedJugadores.length > 20) {
      this.selectedJugadores = this.selectedJugadores.slice(0, 20);
    }
  }

  onSubmit(): void {
    const equipoData = {
        nombre: this.team.nombre,
        logo: this.team.logo,
        direccion: this.team.direccion,
        ciudad: this.team.ciudad,
        provincia: this.team.provincia,
        cant_victorias_local: this.team.cant_victorias_local,
        cant_victorias_visit: this.team.cant_victorias_visit,
        campeonatos: this.team.campeonatos,
        campeones_actuales: this.team.campeones_actuales,
        dt: this.selectedDt ? {  // Verifica si selectedDt no es null
            id: this.selectedDt.id,
            fecha_desde: this.selectedDt.fecha_desde || null,
            fecha_hasta: this.selectedDt.fecha_hasta || null
        } : null,  // Si es null, asigna null
        asistentes: this.selectedAsistentes.length > 0 ? this.selectedAsistentes.map(asistente => ({
            id: asistente.id,
            fecha_desde: asistente.fecha_desde || null,
            fecha_hasta: asistente.fecha_hasta || null
        })) : [],  // Si no hay asistentes, devuelve un array vacío
        jugadores: this.selectedJugadores.length > 0 ? this.selectedJugadores.map(jugador => ({
            id: jugador.id,
            fecha_ingreso: jugador.fecha_ingreso || null,
            fecha_salida: jugador.fecha_salida || null,
            nro_jugador: jugador.nro_jugador || null,
            posicion_pcpal: jugador.posicion_pcpal || null,
            posicion_secundaria: jugador.posicion_secundaria || null
        })) : []  // Si no hay jugadores, devuelve un array vacío
    };

    console.log('Objeto equipoData:', equipoData); // Log de depuración

    this.equiposService.crearEquipo(equipoData).subscribe(
        response => {
            console.log('Equipo creado con éxito', response);
            this.router.navigate(['/']);  // Redirige a la página principal o donde sea necesario
        },
        error => {
            this.errorMessage = error.error.error || 'Error al crear el equipo';  // Captura y muestra el mensaje de error
            console.error('Error al crear equipo', error);
        }
    );
  }
}



