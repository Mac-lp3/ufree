import { Component }      from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { DateRange }      from '../dateRange/dateRange.component'
import { EventService } from '../services/event.service'

@Component({
  selector: 'event',
  host: { class: 'Site-content' },
  templateUrl: 'event.component.html',
  styleUrls:  ['./event.component.sass'],
  providers: [EventService]
})
export class EventComponent {
  eventId: string;
  selectedOption: number;
  dayArray: Day[];

	constructor(private _eventService: EventService, private _route: ActivatedRoute) {
    this.eventId = _route.snapshot.params['id'];
    this.selectedOption = 3;
		_eventService.getEventById(this.eventId).map(this.extractMonthData);
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

  extractMonthData (event: any, error) {
    console.log(event);
    event.attendies.forEach((attendee) => {

    });
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
