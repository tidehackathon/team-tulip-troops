import { HttpClient, HttpHeaders } from '@angular/common/http';
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

  getHeaders() {
    let headers = new HttpHeaders();
    headers = headers.set('kbn-xsrf', 'true');
    return { headers };
  }
  
  analyseArticle(claim: string): Observable<any> {
    const payload = {
      data: claim
    }
    return this.http.post(`${this.baseUrl}/analyse`, payload);
  }

  kibana(): Observable<any> {
    const payload = {
      'url': 'url'
    }
    return this.http.post(`${environment.kibanaUrl}`, payload);
  }

  getClaims(): Observable<any> {
    return this.http.get(`${this.baseUrl}/claims`);
  }
}
