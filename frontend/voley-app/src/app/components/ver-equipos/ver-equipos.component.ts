import { Component, OnInit } from '@angular/core';
import { EquiposService } from '../../services/equipos/equipos.service';
import { Equipo } from '../../models/equipo.model';
import {FormsModule} from "@angular/forms";
import {NgForOf} from "@angular/common";
import {RouterLink} from "@angular/router";
import {HeaderComponent} from "../header/header.component";


@Component({
  selector: 'app-ver-equipos',
  templateUrl: './ver-equipos.component.html',
  standalone: true,
  imports: [
    FormsModule,
    NgForOf,
    RouterLink,
    HeaderComponent
  ],
  styleUrls: ['./ver-equipos.component.css']
})
export class VerEquiposComponent implements OnInit {
  equipos: Equipo[] = [];
  filteredEquipos: Equipo[] = [];
  searchQuery: string = '';

  constructor(private equiposService: EquiposService) {}

  ngOnInit(): void {
    this.equiposService.getEquipos().subscribe(data => {
      this.equipos = data;
      this.filteredEquipos = data;
    });
  }

  onSearchChange(query: string): void {
    this.searchQuery = query;
    this.filteredEquipos = this.equipos.filter(equipo =>
      equipo.nombre.toLowerCase().includes(query.toLowerCase())
    );
  }
}
