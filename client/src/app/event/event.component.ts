import { Component }      from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { DateRange }      from '../dateRange/dateRange.component'

@Component({
  selector: 'event',
  templateUrl: 'event.component.html'
})
export class EventComponent {
  eventId: string;

  constructor(route: ActivatedRoute) {
    this.eventId = route.snapshot.params['id'];
  }
}

export interface Event {
  id: string;
  name: string;
  creator: string;
  dateRanges: DateRange[];
}
