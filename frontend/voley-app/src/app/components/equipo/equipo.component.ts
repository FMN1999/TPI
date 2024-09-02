import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { EquiposService } from '../../services/equipos/equipos.service';
import { FormacionService } from '../../services/formaciones/formaciones.service';
import { NgForOf, NgIf } from "@angular/common";
import { FormsModule } from "@angular/forms";
import {HeaderComponent} from "../header/header.component";

@Component({
  selector: 'app-equipo-detalle',
  templateUrl: './equipo.component.html',
  standalone: true,
  imports: [
    NgIf,
    NgForOf,
    FormsModule,
    HeaderComponent
  ],
  styleUrls: ['./equipo.component.css']
})
export class EquipoDetalleComponent implements OnInit {
  equipo: any = null;
  dts: any[] = [];
  asistentes: any[] = [];
  jugadores: any[] = [];
  showFormacionForm = false;
  formacion: { jugadores: any[], libero: any } = { jugadores: [], libero: null };
  arrayDeIndices: number[] = [0, 1, 2, 3, 4, 5];
  showAgregarDtForm = false;
  showAgregarAsistenteForm = false;
  showAgregarJugadorForm = false;
  nuevoDtId: number | null = null;
  nuevoAsistenteId: number | null = null;
  nuevoJugadorId: number | null = null;
  nuevoJugadorNro: number | null = null;
  nuevoJugadorPosicionPcpal: string = '';
  nuevoJugadorPosicionSecundaria: string = '';
  jugadoresLibres: any[] = [];
  dtsLibres: any[] = [];
  asistentesLibres: any[] = [];
  formaciones: any[] = [];
  formErrorMessage: string | null = null;
  esAsistente = false;
  esDt = false;

  constructor(
    private route: ActivatedRoute,
    private equiposService: EquiposService,
    private formacionService: FormacionService
  ) {}

  ngOnInit(): void {
    const id = +this.route.snapshot.paramMap.get('id')!;
    const idUsuario = +sessionStorage.getItem('user_id')!;
    this.equiposService.getEquipo(id).subscribe(data => {
      this.equipo = data;
      this.dts = data.dts;
      this.asistentes = data.asistentes;
      this.jugadores = data.jugadores;
      this.equiposService.getDtsLibres().subscribe(dts => {
        this.dtsLibres = dts;
      });

      this.equiposService.verificarAsistente(id, idUsuario).subscribe(res => {
        this.esAsistente = res.es_asistente;
      });

      this.equiposService.verificarDt(id, idUsuario).subscribe(res => {
        this.esDt = res.es_dt;
      });

      this.equiposService.getAsistentesLibres().subscribe(asistentes => {
        this.asistentesLibres = asistentes;
      });

      this.equiposService.getJugadoresLibres().subscribe(jugadores => {
        this.jugadoresLibres = jugadores;
      });

      this.formacionService.getFormacionesPorEquipo(id).subscribe(formaciones => {
        this.formaciones = formaciones;
      });
    });

  }

  toggleFormacionForm(): void {
    this.showFormacionForm = !this.showFormacionForm;
  }

  crearFormacion(): void {
    if (this.formacion.jugadores.length < 6) {
      this.formErrorMessage = 'Por favor, selecciona todos los jugadores.';
      return;
    }

    if (new Set(this.formacion.jugadores).size !== this.formacion.jugadores.length) {
      this.formErrorMessage = 'No se puede agregar el mismo jugador más de una vez.';
      return;
    }

    const nuevaFormacion = {
      id_equipo: this.equipo!.id,
      jugadores: this.formacion.jugadores,
      libero: this.formacion.libero
    };

    this.formacionService.crearFormacion(nuevaFormacion).subscribe(
      response => {
        this.formErrorMessage = null;
        this.showFormacionForm = false;
        // Aquí podrías agregar otro mensaje de éxito si lo deseas
      },
      error => {
        this.formErrorMessage = 'Hubo un error al crear la formación.';
      }
    );

    this.formErrorMessage = null;
    this.formacion = { jugadores: [], libero: null };
  }

  darDeBaja(tipo: string, miembroId: number): void {
    if (this.equipo) {
      this.equiposService.darDeBajaMiembro(this.equipo.id, tipo, miembroId).subscribe(
        response => {
          alert('Miembro dado de baja exitosamente');
          this.ngOnInit(); // Recargar la información del equipo
        },
        error => {
          alert('Error al dar de baja el miembro');
        }
      );
    }
  }

  toggleAgregarDtForm(): void {
    this.showAgregarDtForm = !this.showAgregarDtForm;
  }

  toggleAgregarAsistenteForm(): void {
    this.showAgregarAsistenteForm = !this.showAgregarAsistenteForm;
  }

  toggleAgregarJugadorForm(): void {
    this.showAgregarJugadorForm = !this.showAgregarJugadorForm;
  }

  agregarDt(): void {
    if (this.nuevoDtId) {
      this.equiposService.agregarDt(this.equipo!.id, this.nuevoDtId).subscribe(response => {
        alert('DT agregado con éxito');
        this.showAgregarDtForm = false;
      }, error => {
        alert('Error al agregar DT');
      });
    }
  }

  agregarAsistente(): void {
    if (this.nuevoAsistenteId) {
      this.equiposService.agregarAsistente(this.equipo!.id, this.nuevoAsistenteId).subscribe(response => {
        alert('Asistente agregado con éxito');
        this.showAgregarAsistenteForm = false;
      }, error => {
        alert('Error al agregar asistente');
      });
    }
  }

  agregarJugador(): void {
    if (this.nuevoJugadorId && this.nuevoJugadorNro && this.nuevoJugadorPosicionPcpal) {
      const nuevoJugador = {
        nro_jugador: this.nuevoJugadorNro,
        posicion_pcpal: this.nuevoJugadorPosicionPcpal,
        posicion_secundaria: this.nuevoJugadorPosicionSecundaria
      };

      this.equiposService.agregarJugador(this.equipo!.id, this.nuevoJugadorId, nuevoJugador).subscribe(response => {
        alert('Jugador agregado con éxito');
        this.showAgregarJugadorForm = false;
      }, error => {
        alert('Error al agregar jugador');
      });
    }
  }

  eliminarFormacion(id: number): void {
    this.formacionService.eliminarFormacion(id).subscribe(() => {
      this.formaciones = this.formaciones.filter(f => f.id !== id);
    }, error => {
      alert('Hubo un error al eliminar la formación');
    });
  }

}

