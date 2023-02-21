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
