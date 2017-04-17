import { Routes }           from '@angular/router';
import { LandingComponent } from './landing/landing.component';
import { EventComponent }   from './event/event.component';

export const rootRouterConfig: Routes = [
  {
    path: '',
    component: LandingComponent
  },
  {
    path: 'events/:id',
    component: EventComponent
  }
];
