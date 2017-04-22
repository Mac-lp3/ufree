import { Component }      from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { DateRange }      from '../dateRange/dateRange.component'
import { EventService } from '../services/event.service'

@Component({
  selector: 'event',
  host: { class: 'Site-content' },
  templateUrl: 'event.component.html',
  styleUrls:  ['./event.component.css']
})
export class EventComponent {
  eventId: string;

	constuctor(eventService: EventService, route: ActivatedRoute) {
    this.eventId = route.snapshot.params['id'];
		eventService.getEventById(this.eventId).subscribe((event) => {
			console.log(event);
		});
	};
}

export interface Event {
  id: string;
  name: string;
  creator: string;
  dateRanges: DateRange[];
}
