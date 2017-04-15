import { NgModule }      from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { NavbarModule }  from '../decorators/navbar.component';
import { FooterModule }  from '../decorators/footer.component';
import { AppComponent }  from './app.component';

@NgModule({
  imports:      [ BrowserModule ],
  declarations: [ AppComponent, NavbarModule, FooterModule ],
  bootstrap:    [ AppComponent ]
})
export class AppModule { }
