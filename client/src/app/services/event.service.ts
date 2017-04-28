import { Injectable }            from '@angular/core';
import { Http, Headers } from '@angular/http';
import { Event } from '../event/event.component';
import 'rxjs/add/operator/map';

@Injectable()
export class EventService {
  baseUrl: string;
  postHeaders: Headers;

  constructor(private http: Http) {
    this.baseUrl = 'localhost:4000/events/';
    this.postHeaders = new Headers({
      'Content-Type':'application/json'
    });
  }

  getEventById(id: string) {
    return this.makeGetRequest(id);
  }

  createEvent(event: Event) {
    return this.makePostRequest(event);
  }

  private makeGetRequest(id: string) {
    let url = this.baseUrl + id;

    return this.http.get(url).map((res) => {
      return res.json().data || { };
    });
  }

  private makePostRequest(event: Event) {
    let url = this.baseUrl;

    return this.http.post(url, event, {headers: this.postHeaders}).map((res) => {
      return res.json().data || { };
    });
  }
}
