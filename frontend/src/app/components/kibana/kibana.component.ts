import { Component, ElementRef } from '@angular/core';
import { environment } from 'src/environments/environment';

@Component({
  selector: 'app-kibana',
  templateUrl: './kibana.component.html',
  styleUrls: ['./kibana.component.scss']
})
export class KibanaComponent {
  url: string = environment.kibanaUrl;

  constructor(
    private elementRef: ElementRef
    ) {}

  ngOnInit(): void {
    const iframe = this.elementRef.nativeElement.querySelector('#kibana');
    iframe.src = this.url;
  }
}
