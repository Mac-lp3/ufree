import { NgModule }      from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { NavbarModule }  from '../decorators/navbar.component';
import { AppComponent }  from './app.component';

@NgModule({
  imports:      [ BrowserModule ],
  declarations: [ AppComponent, NavbarModule ],
  bootstrap:    [ AppComponent ]
})
export class AppModule { }
