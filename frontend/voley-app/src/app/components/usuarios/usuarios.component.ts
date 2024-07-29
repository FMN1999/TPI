import { Component, OnInit } from '@angular/core';
import { UsuariosService } from '../../services/usuarios/usuarios.service';
import {FormsModule} from "@angular/forms";
import {NgForOf} from "@angular/common";
import {RouterLink} from "@angular/router";

@Component({
  selector: 'app-usuarios',
  templateUrl: './usuarios.component.html',
  standalone: true,
  imports: [
    FormsModule,
    NgForOf,
    RouterLink
  ],
  styleUrls: ['./usuarios.component.css']
})
export class UsuariosComponent implements OnInit {
  usuarios: any[] = [];
  query: string = '';

  constructor(private usuariosService: UsuariosService) {}

  ngOnInit(): void {
    this.obtenerUsuarios();
  }

  obtenerUsuarios(): void {
    this.usuariosService.obtenerUsuarios().subscribe(
      (data: any[]) => {
        this.usuarios = data;
      },
      error => {
        console.error('Error al cargar usuarios:', error);
      }
    );
  }

  buscarUsuarios(): void {
    const term = this.query.toLowerCase();
    this.usuarios = this.usuarios.filter(usuario =>
      usuario.nombre.toLowerCase().includes(term) ||
      usuario.apellido.toLowerCase().includes(term)
    );
  }

  irAlPerfil(usuarioId: number): void {
    // Implementa la lógica para navegar al perfil del usuario
  }
}







