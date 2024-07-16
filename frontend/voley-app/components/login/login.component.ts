import { Component } from '@angular/core';
import { AuthService } from '../auth.service';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html'
})
export class LoginComponent {
  username: string;
  password: string;

  constructor(private authService: AuthService) {}

  login() {
    this.authService.login({username: this.username, password: this.password})
      .subscribe(response => {
        console.log('User logged in successfully', response);
        localStorage.setItem('token', response.token);
      }, error => {
        console.error('Login error', error);
      });
  }
}

