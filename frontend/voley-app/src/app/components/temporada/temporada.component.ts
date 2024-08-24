import { Component, OnInit } from '@angular/core';
import {ActivatedRoute, RouterLink} from '@angular/router';
import { TemporadaService } from '../../services/temporadas/temporadas.service';
import { PosicionesService } from '../../services/posiciones/posiciones.service';
import { EquiposService } from '../../services/equipos/equipos.service';
import { PartidoService } from '../../services/partidos/partidos.service';
import { NgForOf, NgIf } from "@angular/common";
import { FormsModule } from "@angular/forms";

@Component({
  selector: 'app-temporada-detail',
  templateUrl: './temporada.component.html',
  standalone: true,
  imports: [
    NgIf,
    NgForOf,
    FormsModule,
    RouterLink
  ],
  styleUrls: ['./temporada.component.css']
})
export class TemporadaComponent implements OnInit {
  temporada: any;
  posiciones: any[] = [];
  equipos: any[] = [];
  partidos: any[] = [];
  modalAbierto: boolean = false;
  nuevoEquipoId: any;
  nuevoPartido: any = {
    fecha: '',
    hora: '',
    id_local: '',
    id_visita: '',
    set_ganados_local: 0,
    set_ganados_visita: 0
  };

  constructor(
    private route: ActivatedRoute,
    private temporadaService: TemporadaService,
    private posicionesService: PosicionesService,
    private equipoService: EquiposService,
    private partidoService: PartidoService
  ) {}

  ngOnInit(): void {
    const temporadaId = this.route.snapshot.paramMap.get('id');
    if (temporadaId !== null) {
      this.temporadaService.getTemporada(temporadaId).subscribe(data => {
        this.temporada = data;
      });
      this.posicionesService.getPosicionesPorTemporada(temporadaId).subscribe(data => {
        this.posiciones = data;
      });
      this.equipoService.getEquiposTemporada(Number(temporadaId)).subscribe(data => {
        this.equipos = data;
      });
      this.partidoService.getPartidosPorTemporada(temporadaId).subscribe(data => {
        this.partidos = data;
      });
    }
  }

  abrirModal(): void {
    this.modalAbierto = true;
  }

  cerrarModal(): void {
    this.modalAbierto = false;
  }

  agregarPartido(): void {
    const partido = {
      ...this.nuevoPartido,
      id_temporada: this.temporada.id
    };
    this.partidoService.agregarPartido(partido).subscribe(data => {
      this.partidos.push(data);
      this.nuevoPartido = { fecha: '', hora: '', id_local: '', id_visita: '', set_ganados_local: 0, set_ganados_visita: 0 };
      this.cerrarModal();
    });
  }

  agregarEquipo(): void {
    const nuevaPosicion = {
      id_equipo: this.nuevoEquipoId,
      id_temporada: this.temporada.id
    };
    this.posicionesService.agregarEquipoAlaTemporada(nuevaPosicion).subscribe(data => {
      this.posiciones.push(data);
      this.nuevoEquipoId = '';
    });
  }

  eliminarPosicion(id: number): void {
    this.posicionesService.eliminarPosicion(id).subscribe(response => {
      if (response.error) {
        // Mostrar el mensaje de error al usuario
        alert(response.error); // Puedes reemplazar esto con un mensaje más amigable si lo prefieres
      } else {
        // Eliminar la posición de la lista en la UI
        this.posiciones = this.posiciones.filter(posicion => posicion.id !== id);
      }
    });
  }

  eliminarPartido(partidoId: number): void {
    this.partidoService.eliminarPartido(partidoId).subscribe(() => {
      this.partidos = this.partidos.filter(partido => partido.id !== partidoId);
    }, error => {
      console.error('Error al eliminar el partido:', error);
      alert('No se puede eliminar el partido porque los sets ganados no son cero.');
    });
  }

}


