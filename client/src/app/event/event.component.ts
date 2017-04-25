import { Component }      from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { DateRange }      from '../dateRange/dateRange.component'
import { EventService } from '../services/event.service'

@Component({
  selector: 'event',
  host: { class: 'Site-content' },
  templateUrl: 'event.component.html',
  styleUrls:  ['./event.component.sass']
})
export class EventComponent {
  eventId: string;

	constuctor(eventService: EventService, route: ActivatedRoute) {
    this.eventId = route.snapshot.params['id'];
		eventService.getEventById(this.eventId).subscribe((event) => {
			console.log(event);
		});
	};

  createRange(number) {
    var items: number[] = [];
    for(var i = 0; i < number; ++i){
      items.push(i);
    }
    return items;
  };
}

export interface Event {
  id: string;
  name: string;
  creator: string;
  dateRanges: DateRange[];
}
