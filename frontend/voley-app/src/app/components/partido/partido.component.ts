import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { PartidoService } from '../../services/partidos/partidos.service';
import { Partido } from '../../models/partido.model';
import { Set } from '../../models/set.model';
import { Formacion } from '../../models/formacion.model';
import {NgForOf, NgIf, NgOptimizedImage} from "@angular/common";
import { FormsModule } from "@angular/forms";
import {CambioService} from "../../services/cambios/cambios.service";
import {EquiposService} from "../../services/equipos/equipos.service";
import {HeaderComponent} from "../header/header.component";

@Component({
  selector: 'app-partido',
  templateUrl: './partido.component.html',
  standalone: true,
  imports: [
    NgIf,
    FormsModule,
    NgForOf,
    HeaderComponent,
    NgOptimizedImage
  ],
  styleUrls: ['./partido.component.css']
})
export class PartidoComponent implements OnInit {
  partido: Partido={
    id: 0,
    local: '',
    visita: '',
    set_ganados_local: 0,
    set_ganados_visita: 0,
    sets: [],
    fecha: '',
    id_local: 0,
    id_visita: 0,
    estado:'',
    logo_local: '',
    logo_visita:'',
    hora: ''
  };
  nuevoSet: Set = {
    id: 0,
    id_partido: 0,
    puntos_local: 0,
    puntos_visita: 0,
    id_formacion_local: undefined,
    id_formacion_visit: undefined,
  };
  formacionesLocal: Formacion[] = [];
  formacionesVisit: Formacion[] = [];
  nuevoCambio: any = {
    id_jugador_sale: null,
    id_jugador_entra: null,
    id_formacion: null,
    cerro: false,
    permanente: false,
    id_partido: null,
  };
  jugadores: any[] = [];
  cambios: any[] = [];
  res1: boolean | undefined;
  res2: boolean | undefined;
  errorMessage: string='';
  errorMessage2: string='';
  errorMessage3: string='';
  mostrarFormularioCambio: boolean = false; // Controla la visibilidad del formulario


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
      this.partido = data.partido; // Acceder a la propiedad `partido` dentro de `data`

      if (this.partido) {
        this.nuevoSet.id_partido = id;
        if (!this.partido.set_ganados_local) {
          this.partido.set_ganados_local = 0
        }

        if (!this.partido.set_ganados_visita) {
          this.partido.set_ganados_visita = 0
        }

        const idUsuario = +sessionStorage.getItem('user_id')!;

        // Accede correctamente a `id_local` e `id_visita`
        const idLocal = this.partido.id_local;
        const idVisita = this.partido.id_visita;

        this.equipoService.verificarAsistente(idLocal, idUsuario).subscribe(res => {
          this.res1 = res.es_asistente;
        });
        this.equipoService.verificarAsistente(idVisita, idUsuario).subscribe(res => {
          this.res2 = res.es_asistente;
        });


        // Verifica que id_local e id_visita existan y sean números mayores a 0
        if (idLocal && idVisita) {
          this.partidoService.obtenerFormaciones(idLocal).subscribe(
            formaciones => {
              this.formacionesLocal = formaciones;
            },
            error => {
              console.error('Error al cargar formaciones locales:', error);
            }
          );

          this.partidoService.obtenerFormaciones(idVisita).subscribe(
            formaciones => {
              this.formacionesVisit = formaciones;
            },
            error => {
              console.error('Error al cargar formaciones visitantes:', error);
            }
          );
        } else {
          console.error('Los IDs de los equipos local o visitante no están definidos o no son válidos.');
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
        this.cambioService.obtenerCambiosPorPartido(id).subscribe(cambios => {
          this.cambios = cambios;
        });
      }
    });
  }

  agregarSet(): void {
    this.errorMessage='';
    if (this.partido) {
      console.log(this.partido)
      if (this.nuevoSet.puntos_local < 15 && this.nuevoSet.puntos_visita < 15) {
        this.errorMessage='Los sets deben ser mayor a 15. ';
        return;
      }
      if (this.partido.set_ganados_local === 3|| this.partido.set_ganados_visita === 3) {
        this.errorMessage='No se puede agregar más sets, uno de los equipos ya ha ganado 3 sets.';
        return;
      }
      if (this.nuevoSet.puntos_local === this.nuevoSet.puntos_visita) {
        this.errorMessage='No se puede empatar en puntos.';
        return;
      }
      this.partidoService.agregarSet(this.nuevoSet).subscribe(
      data => {
        if (this.partido?.sets) {
          this.partido.sets.push(data);
        }
        window.location.reload();
      },
      error => {
        console.error('Error al agregar set:', error);
      });
    }
  }

  terminarPartido(): void {
    this.errorMessage3='';
    if (this.partido.set_ganados_local && this.partido.set_ganados_visita) {
      if (this.partido.set_ganados_local === this.partido.set_ganados_visita) {
        this.errorMessage3='No se puede terminar el partido con un empate en sets.';
        return;
      }
      if (Math.max(this.partido.set_ganados_local, this.partido.set_ganados_visita) === 1) {
        this.errorMessage3='No se puede terminar el partido si el mayor de los sets ganados es igual a 1.';
        return;
      }
      const id_partido = this.partido.id
      console.log(id_partido)
      this.partidoService.terminarPartido(id_partido).subscribe(
        response => {
          console.log('Partido terminado con éxito:', response);
          window.location.reload();
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
      id_equipo: 0,
      id_partido:0
    };
    this.mostrarFormularioCambio = true;
  }

  registrarCambio(): void {
    this.errorMessage2='';
    if (!this.nuevoCambio.id_formacion || !this.nuevoCambio.id_jugador_sale || !this.nuevoCambio.id_jugador_entra) {
      this.errorMessage2='Por favor, complete todos los campos requeridos antes de registrar el cambio.';
      return;
    }

    this.nuevoCambio.id_partido = this.partido.id
    this.cambioService.registrarCambio(this.nuevoCambio).subscribe(
      response => {
        this.mostrarFormularioCambio = false;
        this.nuevoCambio = {};
        window.location.reload();
      },
      error => {
        console.error('Error al registrar el cambio', error);
      }
    );
  }

  eliminarSet(idSet: number): void {
    if (confirm("¿Estás seguro de que deseas eliminar este set?")) {
      this.partidoService.eliminarSet(idSet).subscribe(
        () => {
          // Remueve el set de la lista en el frontend
          this.partido.sets = this.partido.sets.filter(set => set.id !== idSet);
          console.log(`Set con ID ${idSet} eliminado`);
          window.location.reload();
        },
        error => {
          console.error('Error al eliminar el set:', error);
        }
      );
    }
  }


  cancelarCambio(): void {
    this.mostrarFormularioCambio = false;
  }
}
