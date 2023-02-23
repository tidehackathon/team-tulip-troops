import { Component, OnInit } from '@angular/core';
import { FormControl, Validators } from '@angular/forms';
import { ApiService } from 'src/app/services/api.service';
import { StateService } from 'src/app/services/state.service';
import { trigger, transition, animate, style } from '@angular/animations'
import { interval, Subscription } from 'rxjs';
import { Router } from '@angular/router';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss'],
  animations: [
    trigger('slideInOutInput', [
      transition(':enter', [
        style({transform: 'translateY(-100%)', opacity: '0.0'}),
        animate('500ms 500ms ease-in', style({transform: 'translateY(0%)', opacity: '1.0'}))
      ]),
      transition(':leave', [
        animate('500ms 500ms ease-in', style({transform: 'translateY(-100%)'}))
      ])
    ]),
    trigger('slideInOutLoader', [
      transition(':enter', [
        style({transform: 'translateY(-100%)', opacity: '0.0', height: '0px'}),
        animate('500ms 500ms ease-in', style({transform: 'translateY(0%)', opacity: '1.0', height: '100px'}))
      ]),
      transition(':leave', [
        animate('500ms 500ms ease-in', style({transform: 'translateY(-100%)'}))
      ])
    ]),
  ]
})
export class HomeComponent implements OnInit {
  articalFormControl = new FormControl('', Validators.required);
  isLoading: boolean = false;
  loaderValue: number = 0;
  int = interval(100);
  intervalSubscription: Subscription = new Subscription;
  credibility_label: string = '';

  job1: boolean = true;
  job2: boolean = false;
  job3: boolean = false;
  job4: boolean = false;
  job5: boolean = false;
  job6: boolean = false;
  job7: boolean = false;
  job8: boolean = false;

  job1done: boolean = false;
  job2done: boolean = false;
  job3done: boolean = false;
  job4done: boolean = false;
  job5done: boolean = false;
  job6done: boolean = false;
  job7done: boolean = false;
  job8done: boolean = false;

  allDone: boolean = false;
  resultReceived: boolean = false;

  constructor(
    private api: ApiService,
    private router: Router
  ) {}

  ngOnInit(): void {
    this.reset();
  }

  onSubmit(): void {
    if (this.articalFormControl.valid) {
      this.startLoader();
      this.api.analyseArticle(this.articalFormControl.value as string).subscribe(result => {
        console.log(result);
        this.resultReceived = true;
        this.credibility_label = `${result.credibility.credibility_label} (${String(result.credibility.credibility_score)})`;
        this.loaderValue = this.loaderValue + 25;
      });
    }
  }

  startLoader(): void {
    this.isLoading = true;
    this.intervalSubscription = this.int.subscribe(() => {
      this.loaderValue = this.loaderValue + 0.1;
      if (this.loaderValue > 5) {
        this.job1done = true;
        this.job2 = true;
      }
      if (this.loaderValue > 10) {
        this.job2done = true;
        this.job3 = true;
      }
      if (this.loaderValue > 15) {
        this.job3done = true;
        this.job4 = true;
      }
      if (this.loaderValue > 20) {
        this.job4done = true;
        this.job5 = true;
      }
      if (this.loaderValue > 40) {
        this.job5done = true;
        this.job6 = true;
      }
      if (this.loaderValue > 70) {
        this.job6done = true;
        this.job7 = true;
      }
      if (this.loaderValue > 90) {
        this.job7done = true;
        this.job8 = true;
      }
      if (this.loaderValue > 100) {
        this.job8done = true;
      }
      if (this.loaderValue > 100 && this.resultReceived) {
        this.allDone = true;
      }
    });
  }

  toToDetails(): void {
    this.router.navigateByUrl('/kibana');
  }
  
  reset(): void {
    this.intervalSubscription.unsubscribe();
    this.articalFormControl.reset();
    this.loaderValue = 0;
    this.isLoading = false;
    this.resultReceived = false;
  }
}
