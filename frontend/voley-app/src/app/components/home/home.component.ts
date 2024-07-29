import { Component } from '@angular/core';
import {CarouselComponent} from "../carousel/carousel.component";
import {RouterLink} from "@angular/router";
import { AuthService } from "../../services/auth/auth.service"
import {NgIf} from "@angular/common";
import {HeaderComponent} from "../header/header.component";

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [
    CarouselComponent,
    RouterLink,
    NgIf,
    HeaderComponent
  ],
  templateUrl: './home.component.html',
  styleUrl: './home.component.css'
})
export class HomeComponent {
  constructor(private authService: AuthService) {}

  isLoggedIn(): boolean {
    return this.authService.isAuthenticated();
  }

  logout(): void {
    this.authService.logout();
  }
}
