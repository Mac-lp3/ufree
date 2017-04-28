import { NgModule }         from '@angular/core';
import { RouterModule }     from '@angular/router';
import { rootRouterConfig } from './app.routes';
import { BrowserModule }    from '@angular/platform-browser';
import { NavbarComponent }  from './decorators/navbar.component';
import { FooterComponent }  from './decorators/footer.component';
import { LandingComponent } from './landing/landing.component';
import { EventComponent }   from './event/event.component';
import { AppComponent }     from './app.component';
import { HttpModule } from '@angular/http';


@NgModule({
  imports:      [
    BrowserModule,
    HttpModule,
    RouterModule.forRoot(rootRouterConfig, { useHash: true })
  ],
  declarations: [
    AppComponent,
    NavbarComponent,
    FooterComponent,
    LandingComponent,
    EventComponent
  ],
  bootstrap:    [ AppComponent ]
})
export class AppModule { }
