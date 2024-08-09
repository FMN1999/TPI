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
import {AltaLigaComponent} from "./components/alta-liga/alta-liga.component";
import {VerLigasComponent} from "./components/ver-ligas/ver-ligas.component";
import {LigaComponent} from "./components/liga/liga.component";
import {TemporadaComponent} from "./components/temporada/temporada.component";

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
  { path: 'equipo/:id', component: EquipoDetalleComponent },
  { path: 'alta-liga', component: AltaLigaComponent },
  { path: 'ver-ligas', component: VerLigasComponent },
  { path: 'liga/:id', component: LigaComponent },
  { path: 'temporada/:id', component: TemporadaComponent },

];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule {}

export { routes };

