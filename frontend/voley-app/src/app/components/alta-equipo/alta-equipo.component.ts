import { Component, OnInit } from '@angular/core';
import { EquiposService } from '../../services/equipos/equipos.service';
import { FormsModule, ReactiveFormsModule } from "@angular/forms";
import { NgForOf, NgIf } from "@angular/common";

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

  constructor(private equiposService: EquiposService) {}

  ngOnInit(): void {
    this.getDts();
    this.getAsistentes();
    this.getJugadores();
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
      dt: {
        id: this.selectedDt.id,
        fecha_desde: this.selectedDt.fecha_desde,
        fecha_hasta: this.selectedDt.fecha_hasta
      },
      asistentes: this.selectedAsistentes.map(asistente => ({
        id: asistente.id,
        fecha_desde: asistente.fecha_desde,
        fecha_hasta: asistente.fecha_hasta
      })),
      jugadores: this.selectedJugadores.map(jugador => ({
        id: jugador.id,
        fecha_ingreso: jugador.fecha_ingreso,
        fecha_salida: jugador.fecha_salida,
        nro_jugador: jugador.nro_jugador,
        posicion_pcpal: jugador.posicion_pcpal,
        posicion_secundaria: jugador.posicion_secundaria
      }))
    };

    this.equiposService.crearEquipo(equipoData).subscribe(response => {
      console.log('Equipo creado:', response);
    });
  }
}



