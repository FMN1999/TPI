import { Component, OnInit } from '@angular/core';
import { AuthService } from '../../services/auth/auth.service';
import {RouterLink} from "@angular/router";
import {NgIf} from "@angular/common";

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
  dropdownOpen = false;

  constructor(public authService: AuthService) { }

  ngOnInit(): void { }

  get isAuthenticated(): boolean {
    return this.authService.isAuthenticated();
  }

  toggleDropdown(event: Event): void {
    event.preventDefault();
    this.dropdownOpen = !this.dropdownOpen;
  }

  logout(): void {
    this.authService.logout();
  }
}
