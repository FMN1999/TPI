import { Component, OnInit } from '@angular/core';
import {ActivatedRoute, RouterLink} from '@angular/router';
import { LigaService } from '../../services/ligas/liga.service';
import { TemporadaService } from '../../services/temporadas/temporadas.service';
import {FormsModule} from "@angular/forms";
import {NgForOf, NgIf} from "@angular/common";
import { AuthService } from '../../services/auth/auth.service';
import {HeaderComponent} from "../header/header.component";

@Component({
  selector: 'app-liga-detail',
  templateUrl: './liga.component.html',
  standalone: true,
  imports: [
    FormsModule,
    NgForOf,
    RouterLink,
    NgIf,
    HeaderComponent
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
  successMessage: string = '';
  errorMessage: string = '';
  errorMessage2: string = '';
  tipo: string | undefined;

  constructor(
    private route: ActivatedRoute,
    private ligaService: LigaService,
    private temporadaService: TemporadaService,
    private authService: AuthService
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

    const idUsuario= this.authService.getUsuarioId();

    this.authService.obtenerTipoUsuario(Number(idUsuario)).subscribe((data: { tipo: string; }) => {
      this.tipo = data.tipo;
    });
  }

  agregarTemporada(): void {
    if (this.nuevaTemporada.anio_desde && this.nuevaTemporada.anio_hasta && this.nuevaTemporada.estado) {
      this.temporadaService.crearTemporada(this.nuevaTemporada).subscribe({
        next: (data) => {
          this.temporadas.push(data);
          this.nuevaTemporada = { anio_desde: null, anio_hasta: null, estado: '', id_liga: null }; // Reiniciar el objeto
          this.successMessage = 'Temporada agregada exitosamente!';
        },
        error: (error) => {
          this.errorMessage2 = 'Hubo un problema al agregar la temporada. Inténtalo de nuevo.';
        }
      });
    } else {
      this.errorMessage2 = 'Por favor, completa todos los campos correctamente.';
    }
  }


  eliminarTemporada(id: number): void {
    this.temporadaService.eliminarTemporada(id).subscribe(
      response => {
        this.successMessage = 'Temporada eliminada con éxito';
        this.errorMessage = '';
        // Actualizar la lista de temporadas
        this.temporadas = this.temporadas.filter(temporada => temporada.id !== id);
      },
      error => {
        this.errorMessage = error.error.error || 'Error al eliminar la temporada';
        this.successMessage = '';
      }
    );
  }
}


