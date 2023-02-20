import { Component, HostBinding } from '@angular/core';
import { FormControl } from '@angular/forms';
import { Router } from '@angular/router';
import { StateService } from './services/state.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent {
  isLoading: boolean = false;
  toggleTheme = new FormControl(false);

  @HostBinding('class') className = '';

  constructor(
    private state: StateService,
    private router: Router
  ) {
    this.state.isLoading.subscribe(loading => {
      this.isLoading = loading;
    });

    this.toggleTheme.valueChanges.subscribe((darkMode) => {
      const darkClassName = 'darkMode';
      this.className = darkMode ? darkClassName : '';
    });
  }

  home(): void {
    this.router.navigateByUrl('/');
  }


}
