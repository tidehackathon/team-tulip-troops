import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { HomeComponent } from './components/home/home.component';
import { KibanaComponent } from './components/kibana/kibana.component';
import { ResultDetailsComponent } from './components/result-details/result-details.component';
import { ResultComponent } from './components/result/result.component';

const routes: Routes = [
  { path: '', redirectTo: 'home', pathMatch: 'full' },
  { path: 'home', component: HomeComponent },
  { path: 'result', component: ResultComponent },
  { path: 'result/:id', component: ResultDetailsComponent },
  { path: 'kibana', component: KibanaComponent },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
