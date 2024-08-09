import { Component, OnInit } from '@angular/core';
import {ActivatedRoute, RouterLink} from '@angular/router';
import { LigaService } from '../../services/ligas/liga.service';
import { TemporadaService } from '../../services/temporadas/temporadas.service';
import {FormsModule} from "@angular/forms";
import {NgForOf} from "@angular/common";

@Component({
  selector: 'app-liga-detail',
  templateUrl: './liga.component.html',
  standalone: true,
  imports: [
    FormsModule,
    NgForOf,
    RouterLink
  ],
  styleUrls: ['./liga.component.css']
})
export class LigaComponent implements OnInit {
  liga: any;
  temporadas: any[] = [];
  nuevaTemporada = {
    anio_desde: null,
    anio_hasta: null,
    estado: '',
    id_liga: null
  };

  constructor(
    private route: ActivatedRoute,
    private ligaService: LigaService,
    private temporadaService: TemporadaService
  ) { }

  ngOnInit(): void {
    const ligaId = this.route.snapshot.paramMap.get('id');
    if (ligaId !== null) {
      // @ts-ignore
      this.nuevaTemporada.id_liga = ligaId;
      this.ligaService.obtenerLigaPorId(ligaId).subscribe(data => {
        this.liga = data;
      });
      this.temporadaService.getTemporadasPorLiga(ligaId).subscribe(data => {
        this.temporadas = data;
      });
    }
  }

  agregarTemporada(): void {
    this.temporadaService.crearTemporada(this.nuevaTemporada).subscribe(data => {
      this.temporadas.push(data);
      this.nuevaTemporada.anio_desde = null;
      this.nuevaTemporada.anio_hasta = null;
      this.nuevaTemporada.estado = '';
    });
  }
}


