import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { StateService } from './services/state.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent {
  isLoading: boolean = false;

  constructor(
    private state: StateService,
    private router: Router
  ) {
    this.state.isLoading.subscribe(loading => {
      this.isLoading = loading;
    });
  }

  home(): void {
    this.router.navigateByUrl('/');
  }
}
