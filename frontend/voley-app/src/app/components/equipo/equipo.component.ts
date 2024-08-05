import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { EquiposService } from '../../services/equipos/equipos.service';
import { Equipo } from '../../models/equipo.model';
import {NgIf} from "@angular/common";

@Component({
  selector: 'app-equipo-detalle',
  templateUrl: './equipo.component.html',
  standalone: true,
  imports: [
    NgIf
  ],
  styleUrls: ['./equipo.component.css']
})
export class EquipoDetalleComponent implements OnInit {
  equipo: Equipo | null = null;

  constructor(
    private route: ActivatedRoute,
    private equiposService: EquiposService
  ) {}

  ngOnInit(): void {
    const id = +this.route.snapshot.paramMap.get('id')!;
    this.equiposService.getEquipo(id).subscribe(data => {
      this.equipo = data;
    });
  }
}
