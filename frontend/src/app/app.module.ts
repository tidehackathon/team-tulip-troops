import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { MaterialModule } from './material/material.module';
import { HomeComponent } from './components/home/home.component';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { ResultComponent } from './components/result/result.component';
import { HttpClientModule } from '@angular/common/http';
import { KibanaComponent } from './components/kibana/kibana.component';
import { ResultDetailsComponent } from './components/result-details/result-details.component';

@NgModule({
  declarations: [
    AppComponent,
    HomeComponent,
    ResultComponent,
    KibanaComponent,
    ResultDetailsComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    BrowserAnimationsModule,
    MaterialModule,
    FormsModule,
    ReactiveFormsModule,
    HttpClientModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
