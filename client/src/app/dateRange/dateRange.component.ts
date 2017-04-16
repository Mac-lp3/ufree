import { Component } from '@angular/core';

@Component({})
export class DateRangeComponent {

}

export interface DateRange {
  id: string;
  name: string;
  from: string;
  to: string;
}
