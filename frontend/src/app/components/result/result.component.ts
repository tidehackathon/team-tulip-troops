import { Component, OnInit } from '@angular/core';
import { ApiService } from 'src/app/services/api.service';

@Component({
  selector: 'app-result',
  templateUrl: './result.component.html',
  styleUrls: ['./result.component.scss'],
})
export class ResultComponent implements OnInit {

  claims = [];
  columns = ['claim', 'score'];

  constructor(
    private api: ApiService
  ) {}

  ngOnInit(): void {
    // this.api.getClaims().subscribe(claims => {
    //   console.log(claims);
    //   this.claims = claims;
    // });
  }
}
