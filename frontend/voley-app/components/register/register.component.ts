import { Component } from '@angular/core';
import { AuthService } from '../auth.service';

@Component({
  selector: 'app-register',
  templateUrl: './register.component.html'
})
export class RegisterComponent {
  username: string;
  email: string;
  password: string;

  constructor(private authService: AuthService) {}

  register() {
    this.authService.register({username: this.username, email: this.email, password: this.password})
      .subscribe(response => {
        console.log('User registered successfully', response);
      }, error => {
        console.error('Registration error', error);
      });
  }
}

