import { Component, OnInit } from '@angular/core';
import { AuthService } from '../../services/auth/auth.service';
import { RouterLink, Router  } from "@angular/router";
import { NgIf } from "@angular/common";
import { Location } from '@angular/common';

@Component({
  selector: 'app-header',
  templateUrl: './header.component.html',
  standalone: true,
  imports: [
    RouterLink,
    NgIf
  ],
  styleUrls: ['./header.component.css']
})
export class HeaderComponent implements OnInit {
  dropdownOpen: { [key in 'usuario' | 'equipos' | 'ligas' | 'partidos']: boolean } = {
    usuario: false,
    equipos: false,
    ligas: false,
    partidos: false
  };
  tipo: string | undefined;
  sidebarOpen = false;

  constructor(public authService: AuthService, private location: Location, private router: Router) { }

  ngOnInit(): void {
    if (this.isAuthenticated){
      const id = this.authService.getUsuarioId();
      this.authService.obtenerTipoUsuario(Number(id)).subscribe(
          response => {
            this.tipo = response.tipo;
          });
    }
  }

  get isAuthenticated(): boolean {
    return this.authService.isAuthenticated();
  }

  goBack() {
    const currentUrl = this.router.url;
    if (currentUrl === '/login' || currentUrl === '/register') {
      this.router.navigate(['/']);
    } else {
      this.location.back();
    }
  }

  getUsuarioId(): string | null {
    return this.authService.getUsuarioId();
  }

  toggleDropdown(event: Event, dropdown: 'usuario' | 'equipos' | 'ligas' | 'partidos'): void {
    event.preventDefault();
    this.dropdownOpen[dropdown] = !this.dropdownOpen[dropdown];
  }

  toggleSidebar() {
    this.sidebarOpen = !this.sidebarOpen;
  }

  logout(): void {
    this.authService.logout();
    this.router.navigate(['/']).then(r => {});
    window.location.reload();
  }
}

