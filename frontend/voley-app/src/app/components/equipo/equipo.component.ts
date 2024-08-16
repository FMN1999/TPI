import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { EquiposService } from '../../services/equipos/equipos.service';
import { FormacionService } from '../../services/formaciones/formaciones.service';
import { Equipo } from '../../models/equipo.model';
import {NgForOf, NgIf} from "@angular/common";
import {Jugador} from "../../models/user.model";
import {FormsModule} from "@angular/forms";

@Component({
  selector: 'app-equipo-detalle',
  templateUrl: './equipo.component.html',
  standalone: true,
  imports: [
    NgIf,
    NgForOf,
    FormsModule
  ],
  styleUrls: ['./equipo.component.css']
})
export class EquipoDetalleComponent implements OnInit {
  equipo: Equipo | null = null;
  jugadores: Jugador[] = [];
  showFormacionForm = false;
  formacion: { jugadores: any[], libero: any } = { jugadores: [], libero: null };
  arrayDeIndices: number[] = [0, 1, 2, 3, 4, 5];

  constructor(
    private route: ActivatedRoute,
    private equiposService: EquiposService,
    private formacionService: FormacionService
  ) {}

  ngOnInit(): void {
    const id = +this.route.snapshot.paramMap.get('id')!;
    this.equiposService.getEquipo(id).subscribe(data => {
      this.equipo = data;

      // Obtener los jugadores del equipo
      this.equiposService.getJugadoresPorEquipo(id).subscribe(jugadores => {
        this.jugadores = jugadores;
      });
    });
  }

  toggleFormacionForm(): void {
    this.showFormacionForm = !this.showFormacionForm;
  }

  crearFormacion(): void {
    if (this.formacion.jugadores.length < 6) {
      alert('Por favor, selecciona todos los jugadores.');
      return;
    }

    const nuevaFormacion = {
      id_equipo: this.equipo!.id,
      jugadores: this.formacion.jugadores,
      libero: this.formacion.libero
    };
    console.log('Datos que se envían al backend:', nuevaFormacion);

    this.formacionService.crearFormacion(nuevaFormacion).subscribe(response => {
      alert('Formación creada con éxito');
      this.showFormacionForm = false;
    }, error => {
      alert('Hubo un error al crear la formación');
    });

    this.showFormacionForm = false;
    this.formacion = { jugadores: [], libero: null };
  }
}
