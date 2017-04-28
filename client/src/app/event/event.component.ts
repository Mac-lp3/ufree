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
  selectedOption: number;
  dayArray: Day[];

	constuctor(eventService: EventService, route: ActivatedRoute) {
    this.eventId = route.snapshot.params['id'];
    this.selectedOption = 3;
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

  setOption(value) {
    console.log('Cliqued ' + value);
    if (value <= 3 && value >= 0) {
      this.selectedOption = value;
    }
  };
}

export interface Day {
  red: number;
  yellow: number;
  blue: number;
}

export interface Event {
  id: string;
  name: string;
  creator: string;
  dateRanges: DateRange[];
}
