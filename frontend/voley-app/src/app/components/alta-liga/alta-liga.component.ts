import { Component, OnInit } from '@angular/core';
import { LigaService } from '../../services/ligas/liga.service';
import {FormsModule} from "@angular/forms";

@Component({
  selector: 'app-alta-liga',
  templateUrl: './alta-liga.component.html',
  standalone: true,
  imports: [
    FormsModule
  ],
  styleUrls: ['./alta-liga.component.css']
})
export class AltaLigaComponent implements OnInit {
  liga: any = {
    categoria: '',
    ptos_x_victoria: 0,
    ptos_x_32_vict: 0,
    ptos_x_32_derrota: 0
  };

  constructor(private ligaService: LigaService) {}

  ngOnInit(): void {}

  onSubmit(): void {
    this.ligaService.crearLiga(this.liga).subscribe(response => {
      console.log('Liga creada:', response);
    }, error => {
      console.error('Error al crear la liga:', error);
    });
  }
}


