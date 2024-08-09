import { Component, OnInit } from '@angular/core';
import { LigaService } from '../../services/ligas/liga.service';
import {FormsModule} from "@angular/forms";
import {RouterLink} from "@angular/router";
import {NgForOf} from "@angular/common";

@Component({
  selector: 'app-ver-ligas',
  templateUrl: './ver-ligas.component.html',
  standalone: true,
  imports: [
    FormsModule,
    RouterLink,
    NgForOf
  ],
  styleUrls: ['./ver-ligas.component.css']
})
export class VerLigasComponent implements OnInit {
  ligas: any[] = [];
  searchTerm: string = '';

  constructor(private ligaService: LigaService) {}

  ngOnInit(): void {
    this.obtenerLigas();
  }

  obtenerLigas(): void {
    this.ligaService.obtenerLigas().subscribe(data => {
      this.ligas = data;
    }, error => {
      console.error('Error al obtener las ligas:', error);
    });
  }

  onSearch(): void {
    if (this.searchTerm) {
      this.ligas = this.ligas.filter(liga => liga.categoria.toLowerCase().includes(this.searchTerm.toLowerCase()));
    } else {
      this.obtenerLigas(); // Re-fetch the list if search term is empty
    }
  }
}
