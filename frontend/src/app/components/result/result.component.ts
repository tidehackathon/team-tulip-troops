import { Component, ElementRef, OnInit } from '@angular/core';
import { environment } from 'src/environments/environment';

@Component({
  selector: 'app-result',
  templateUrl: './result.component.html',
  styleUrls: ['./result.component.scss'],
})
export class ResultComponent implements OnInit {
  url: string = environment.kibanaUrl;

  constructor(
    private elementRef: ElementRef
    ) {}

  ngOnInit(): void {
    const iframe = this.elementRef.nativeElement.querySelector('#kibana');
    iframe.src = this.url;
  }
}
