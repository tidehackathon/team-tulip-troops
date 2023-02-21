import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class StateService {

  private isLoadingSource = new BehaviorSubject<boolean>(false);
  isLoading = this.isLoadingSource.asObservable();

  constructor() { }

  setIsLoading(value: boolean): void {
    this.isLoadingSource.next(value);
  }

}
