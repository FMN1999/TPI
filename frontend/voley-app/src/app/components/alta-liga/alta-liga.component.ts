import { Component, OnInit } from '@angular/core';
import { LigaService } from '../../services/ligas/liga.service';
import { FormsModule } from "@angular/forms";
import {NgIf} from "@angular/common";

@Component({
  selector: 'app-alta-liga',
  templateUrl: './alta-liga.component.html',
  standalone: true,
  imports: [
    FormsModule,
    NgIf
  ],
  styleUrls: ['./alta-liga.component.css']
})
export class AltaLigaComponent implements OnInit {
  liga: any = {
    nombre: '',
    categoria: '',
    ptos_x_victoria: 0,
    ptos_x_32_vict: 0,
    ptos_x_32_derrota: 0
  };

  errorMessage: string = '';
  successMessage: string = '';

  constructor(private ligaService: LigaService) {}

  ngOnInit(): void {}

  onSubmit(): void {
    this.ligaService.crearLiga(this.liga).subscribe(
      response => {
        this.successMessage = 'Liga creada con éxito';
        this.errorMessage = '';
        console.log('Liga creada:', response);
      },
      error => {
        this.errorMessage = error.error.error || 'Error al crear la liga';
        this.successMessage = '';
        console.error('Error al crear la liga:', error);
      }
    );
  }
}
