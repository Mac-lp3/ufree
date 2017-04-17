import { Component } from '@angular/core';

@Component({
  selector: 'my-app',
  host: { class: 'Site-content' },
  template: `
    <navbar></navbar>
    <router-outlet></router-outlet>
    <ufooter></ufooter>
  `
})
export class AppComponent { }
