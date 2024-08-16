  import { Component, OnInit } from '@angular/core';
  import { ActivatedRoute } from '@angular/router';
  import { PartidoService } from '../../services/partidos/partidos.service';
  import { Partido } from '../../models/partido.model';
  import { Set } from '../../models/set.model';
  import { Formacion } from '../../models/formacion.model';
  import { NgForOf, NgIf } from "@angular/common";
  import { FormsModule } from "@angular/forms";
  import {CambioService} from "../../services/cambios/cambios.service";
  import {EquiposService} from "../../services/equipos/equipos.service";

  @Component({
    selector: 'app-partido',
    templateUrl: './partido.component.html',
    standalone: true,
    imports: [
      NgIf,
      FormsModule,
      NgForOf
    ],
    styleUrls: ['./partido.component.css']
  })
  export class PartidoComponent implements OnInit {
    partido: Partido | undefined;
    nuevoSet: Set = {
      id: 0,
      id_partido: 0,
      puntos_local: 0,
      puntos_visita: 0,
      id_formacion_local: undefined,
      id_formacion_visit: undefined
    };
    formacionesLocal: Formacion[] = [];
    formacionesVisit: Formacion[] = [];
    nuevoCambio: any = {
      id_jugador_sale: null,
      id_jugador_entra: null,
      id_formacion: null,
      cerro: false,
      permanente: false,
    };
    jugadores: any[] = [];  // Lista de jugadores del equipo seleccionado


    constructor(
      private route: ActivatedRoute,
      private partidoService: PartidoService,
      private cambioService: CambioService,
      private equipoService: EquiposService
    ) {
    }

    ngOnInit(): void {
      const id = +this.route.snapshot.paramMap.get('id')!;
      this.partidoService.getDetallesPartido(id).subscribe(data => {
        this.partido = data[0];
        if (this.partido) {
          this.nuevoSet.id_partido = id;

          if (this.partido.id_local && this.partido.id_visita) {
            this.partidoService.obtenerFormaciones(this.partido.id_local).subscribe(
              formaciones => {
                this.formacionesLocal = formaciones;
              },
              error => {
                console.error('Error al cargar formaciones locales:', error);
              }
            );

            this.partidoService.obtenerFormaciones(this.partido.id_visita).subscribe(
              formaciones => {
                this.formacionesVisit = formaciones;
              },
              error => {
                console.error('Error al cargar formaciones visitantes:', error);
              }
            );
          } else {
            console.error('Los IDs de los equipos local o visitante no están definidos.');
          }

          // Obtener los sets existentes para el partido
          this.partidoService.obtenerSets(id).subscribe(
            sets => {
              this.partido!.sets = sets;
            },
            error => {
              console.error('Error al obtener los sets:', error);
            }
          );
        }
      });
    }


    agregarSet(): void {
      if (this.partido) {
        this.partidoService.agregarSet(this.nuevoSet).subscribe(
          data => {
            if (this.partido?.sets) {
              this.partido.sets.push(data);
            }
          },
          error => {
            console.error('Error al agregar set:', error);
          }
        );
      }
    }


    terminarPartido(): void {
      if (this.partido) {
        this.partidoService.terminarPartido(this.partido.id).subscribe(
          response => {
            console.log('Partido terminado con éxito:', response);
          },
          error => {
            console.error('Error al terminar el partido:', error);
          }
        );
      }
    }

    onFormacionChange(): void {
      console.log('ID de la formación seleccionada:', this.nuevoCambio.id_formacion);

      // Depuración de formaciones locales y visitantes
      console.log('Formaciones Local:', this.formacionesLocal);
      console.log('Formaciones Visit:', this.formacionesVisit);

      // Combinar formaciones locales y visitantes
      const todasLasFormaciones = [...this.formacionesLocal, ...this.formacionesVisit];

      // Mostrar todas las formaciones para verificar su estructura
      console.log('Todas las formaciones:', todasLasFormaciones);

      // Convertir IDs a números para asegurar comparación correcta
      const formacionSeleccionada = todasLasFormaciones.find(f => {
        const formacionId = Number(f.id); // Convertir ID de la formación a número
        const cambioId = Number(this.nuevoCambio.id_formacion); // Convertir el ID del cambio a número
        console.log('Comparando:', formacionId, 'con', cambioId); // Depuración de comparación
        return formacionId === cambioId;
      });

      console.log('Formación seleccionada:', formacionSeleccionada);

      if (formacionSeleccionada) {
        this.equipoService.getJugadoresPorEquipo(formacionSeleccionada.id_equipo).subscribe(
          jugadores => {
            this.jugadores = jugadores;
            console.log('Jugadores cargados:', this.jugadores);
          },
          error => console.error('Error al cargar jugadores del equipo', error)
        );
      } else {
        console.error('No se encontró la formación seleccionada.');
      }
    }


    abrirFormularioCambio(): void {
      this.nuevoCambio = {
        id_jugador_sale: null,
        id_jugador_entra: null,
        id_formacion: null,
        cerro: false,
        permanente: false,
        id_equipo: 0
      };
    }

    registrarCambio(): void {
      this.cambioService.registrarCambio(this.nuevoCambio).subscribe(
        response => {
          console.log('Cambio registrado con éxito', response);
          // Aquí puedes actualizar la interfaz según sea necesario
        },
        error => {
          console.error('Error al registrar el cambio', error);
        }
      );
    }
  }
