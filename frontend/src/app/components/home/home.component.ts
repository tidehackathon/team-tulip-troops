import { Component } from '@angular/core';
import { FormControl, Validators } from '@angular/forms';
import { ApiService } from 'src/app/services/api.service';
import { StateService } from 'src/app/services/state.service';
import { trigger, transition, animate, style } from '@angular/animations'
import { interval } from 'rxjs';
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
export class HomeComponent {
  articalFormControl = new FormControl('', Validators.required);
  isLoading: boolean = false;
  loaderValue: number = 0;
  int = interval(100);

  job1: boolean = true;
  job2: boolean = false;
  job3: boolean = false;
  job4: boolean = false;
  job5: boolean = false;
  job6: boolean = false;

  job1done: boolean = false;
  job2done: boolean = false;
  job3done: boolean = false;
  job4done: boolean = false;
  job5done: boolean = false;
  job6done: boolean = false;

  constructor(
    private api: ApiService,
    private state: StateService,
    private router: Router
  ) {}

  onSubmit(): void {
    this.isLoading = !this.isLoading;
    this.startLoader();
    // if (this.articalFormControl.valid) {
    //   this.state.setIsLoading(true);
    //   this.api.analyseArticle(this.articalFormControl.value as string).subscribe(result => {
    //     console.log(result);
        
    //     // navigate to result page

    //     // Loading false
    //     this.state.setIsLoading(false);
    //   });
    // }
  }

  startLoader(): void {
    const subscription = this.int.subscribe(() => {
      this.loaderValue = this.loaderValue + 0.1;
      if (this.loaderValue > 20) {
        this.job1done = true;
        this.job2 = true;
      }
      if (this.loaderValue > 40) {
        this.job2done = true;
        this.job3 = true;
      }
      if (this.loaderValue > 60) {
        this.job3done = true;
        this.job4 = true;
      }
      if (this.loaderValue > 80) {
        this.job4done = true;
        this.job5 = true;
      }
      if (this.loaderValue > 100) {
        this.resetLoader();
        subscription.unsubscribe();
        this.router.navigateByUrl('/result');
      }
    });
  }
  
  resetLoader(): void {
    this.loaderValue = 0;
  }
}
