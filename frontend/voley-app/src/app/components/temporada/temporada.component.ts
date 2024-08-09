import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
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
    FormsModule
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
      this.equipoService.getEquipos().subscribe(data => {
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

}


