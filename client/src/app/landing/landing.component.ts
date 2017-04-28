import { Component }    from '@angular/core';
import { Router }       from '@angular/router';
import { EventService } from '../services/event.service'

@Component({
  selector: 'landing',
  host: { class: 'Site-content' },
  templateUrl: 'landing.component.html',
  styleUrls:  ['./landing.component.sass']
})
export class LandingComponent {

  constructor(private _eventService: EventService, private _router: Router) {

  }

  postEvent() {
    let id = '101010101';
    this._router.navigate(['events/' + id]);
  }
}
