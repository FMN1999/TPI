import { Component, OnInit } from '@angular/core';
import { UsuariosService } from '../../services/usuarios/usuarios.service';
import { FormsModule } from "@angular/forms";
import { NgForOf } from "@angular/common";
import { RouterLink } from "@angular/router";
import {HeaderComponent} from "../header/header.component";

@Component({
  selector: 'app-usuarios',
  templateUrl: './usuarios.component.html',
  standalone: true,
  imports: [
    FormsModule,
    NgForOf,
    RouterLink,
    HeaderComponent
  ],
  styleUrls: ['./usuarios.component.css']
})
export class UsuariosComponent implements OnInit {
  usuarios: any[] = [];
  todosLosUsuarios: any[] = [];
  query: string = '';

  constructor(private usuariosService: UsuariosService) {}

  ngOnInit(): void {
    this.obtenerUsuarios();
  }

  obtenerUsuarios(): void {
    this.usuariosService.obtenerUsuarios().subscribe(
      (data: any[]) => {
        this.usuarios = data;
        this.todosLosUsuarios = data; // Guardar la lista completa
      },
      error => {
        console.error('Error al cargar usuarios:', error);
      }
    );
  }

  buscarUsuarios(): void {
    const term = this.query.toLowerCase();

    if (term) {
      // Filtrar usuarios cuando hay un término de búsqueda
      this.usuarios = this.todosLosUsuarios.filter(usuario =>
        usuario.nombre.toLowerCase().includes(term) ||
        usuario.apellido.toLowerCase().includes(term)
      );
    } else {
      // Si no hay término de búsqueda, mostrar todos los usuarios
      this.usuarios = [...this.todosLosUsuarios];
    }
  }
}







