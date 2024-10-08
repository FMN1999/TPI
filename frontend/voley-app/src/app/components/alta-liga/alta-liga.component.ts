import { Component, OnInit } from '@angular/core';
import { LigaService } from '../../services/ligas/liga.service';
import { FormsModule } from "@angular/forms";
import {NgIf} from "@angular/common";
import { AuthService } from '../../services/auth/auth.service';
import {Router} from "@angular/router";
import {HeaderComponent} from "../header/header.component";

@Component({
  selector: 'app-alta-liga',
  templateUrl: './alta-liga.component.html',
  standalone: true,
  imports: [
    FormsModule,
    NgIf,
    HeaderComponent
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
  tipo: string | undefined;

  constructor(private ligaService: LigaService, private authService: AuthService, private router: Router) {}

  ngOnInit(): void {
    const idUsuario= this.authService.getUsuarioId();

    this.authService.obtenerTipoUsuario(Number(idUsuario)).subscribe((data: { tipo: string; }) => {
      this.tipo = data.tipo;
    });
  }

  onSubmit(): void {
    if (!this.liga.nombre || !this.liga.categoria ||
        this.liga.ptos_x_victoria === undefined || this.liga.ptos_x_victoria === null ||
        this.liga.ptos_x_32_vict === undefined || this.liga.ptos_x_32_vict === null ||
        this.liga.ptos_x_32_derrota === undefined || this.liga.ptos_x_32_derrota === null) {
        this.errorMessage = 'Por favor, complete todos los campos obligatorios.';
        this.successMessage = '';
        return;
    }

    this.ligaService.crearLiga(this.liga).subscribe(
      response => {
        this.successMessage = 'Liga creada con éxito';
        this.errorMessage = '';
      },
      error => {
        this.errorMessage = error.error.error || 'Error al crear la liga';
        this.successMessage = '';
      }
    );
  }
}
