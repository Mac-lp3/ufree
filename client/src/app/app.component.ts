import { Component } from '@angular/core';

@Component({
  selector: 'my-app',
  template: `
    <navbar></navbar>
    <router-outlet></router-outlet>
    <ufooter></ufooter>
  `
})
export class AppComponent { }
