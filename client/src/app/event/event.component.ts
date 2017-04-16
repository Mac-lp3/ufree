import { Component } from '@angular/core';
import { DateRange } from '../dateRange/dateRange.component'
import { EventService } from '../services/event.service'

@Component({
  selector: 'event',
  templateUrl: 'event.component.html'
})
export class EventComponent {
	constuctor(eventService: EventService ) {
		eventService.getEventById("1").subscribe((event) => {
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
