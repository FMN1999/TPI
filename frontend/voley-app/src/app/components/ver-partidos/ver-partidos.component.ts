import { Component, OnInit } from '@angular/core';
import { PartidoService } from '../../services/partidos/partidos.service';
import { Partido } from '../../models/partido.model';
import {DatePipe, NgForOf} from "@angular/common";
import { Router } from '@angular/router';
import {HeaderComponent} from "../header/header.component";


@Component({
  selector: 'app-ver-partidos',
  templateUrl: './ver-partidos.component.html',
  standalone: true,
  imports: [
    NgForOf,
    DatePipe,
    HeaderComponent
  ],
  styleUrls: ['./ver-partidos.component.css']
})
export class VerPartidosComponent implements OnInit {
  partidos: any[] = [];

  constructor(private partidosService: PartidoService, private router: Router) {}

  ngOnInit(): void {
    this.partidosService.getPartidosSinSetsGanados().subscribe(data => {
      this.partidos = data;
    });
  }

  verDetalles(partidoId: number): void {
    this.router.navigate(['/partido', partidoId]);  // Redirige a la página de detalles del partido
  }
}

