import { Component } from '@angular/core';
import { FormControl, Validators } from '@angular/forms';
import { ApiService } from 'src/app/services/api.service';
import { StateService } from 'src/app/services/state.service';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss'],
})
export class HomeComponent {
  articalFormControl = new FormControl('', Validators.required);

  constructor(
    private api: ApiService,
    private state: StateService
  ) {

  }

  onSubmit(): void {
    if (this.articalFormControl.valid) {
      this.state.setIsLoading(true);
      this.api.analyseArticle(this.articalFormControl.value as string).subscribe(result => {
        console.log(result);
        
  
        // navigate to result page

        // Loading false
      });
    }
  }
}
