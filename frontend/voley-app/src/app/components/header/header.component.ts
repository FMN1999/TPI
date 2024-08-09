import { Component, OnInit } from '@angular/core';
import { AuthService } from '../../services/auth/auth.service';
import { RouterLink } from "@angular/router";
import { NgIf } from "@angular/common";

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
  dropdownOpen: { [key in 'usuario' | 'equipos' | 'ligas']: boolean } = {
    usuario: false,
    equipos: false,
    ligas: false
  };

  constructor(public authService: AuthService) { }

  ngOnInit(): void { }

  get isAuthenticated(): boolean {
    return this.authService.isAuthenticated();
  }

  toggleDropdown(event: Event, dropdown: 'usuario' | 'equipos' | 'ligas'): void {
    event.preventDefault();
    this.dropdownOpen[dropdown] = !this.dropdownOpen[dropdown];
  }

  logout(): void {
    this.authService.logout();
  }
}

