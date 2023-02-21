import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { environment } from 'src/environments/environment';

@Injectable({
  providedIn: 'root'
})
export class ApiService {

  baseUrl: string = environment.apiUrl;

  constructor(
    private http: HttpClient
  ) { }
  
  analyseArticle(url: string): Observable<any> {
    const payload = {
      url
    }
    return this.http.post(`${this.baseUrl}/analyse`, payload);
  }
}
