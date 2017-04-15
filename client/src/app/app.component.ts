import { Component } from '@angular/core';

@Component({
  selector: 'my-app',
  template: `
  <navbar></navbar>
  <h1>Hello {{name}}</h1>
  <router-outlet></router-outlet>
  <ufooter></ufooter>
  `
})
export class AppComponent { name = 'Angular'; }
