import { Component } from '@angular/core';
import { DateRange } from '../dateRange/dateRange.component'

@Component({
  selector: 'event',
  templateUrl: 'event.component.html'
})
export class EventComponent {

}

export interface Event {
  id: string;
  name: string;
  creator: string;
  dateRanges: DateRange[];
}
