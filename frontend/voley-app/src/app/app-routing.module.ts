import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { LoginComponent } from './components/login/login.component';
import { PerfilComponent } from './components/perfil/perfil.component';
import { UsuariosComponent } from './components/usuarios/usuarios.component';
import {HomeComponent} from "./components/home/home.component";
import {RegisterComponent} from "./components/register/register.component";
import {AltaEquipoComponent} from "./components/alta-equipo/alta-equipo.component";
import {VerEquiposComponent} from "./components/ver-equipos/ver-equipos.component";
import {EquipoDetalleComponent} from "./components/equipo/equipo.component";

const routes: Routes = [
  { path: '', component:HomeComponent },
  { path: 'login', component: LoginComponent },
  { path: 'register', component: RegisterComponent },
  { path: 'perfil', component: PerfilComponent },
  { path: 'perfil/:id', component: PerfilComponent },
  { path: 'usuarios', component: UsuariosComponent },
  { path: 'logout', redirectTo: '/login', pathMatch: 'full' },
  { path: 'alta-equipo', component: AltaEquipoComponent },
  { path: 'ver-equipos', component: VerEquiposComponent },
  { path: 'equipo/:id', component: EquipoDetalleComponent }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule {}

export { routes };

