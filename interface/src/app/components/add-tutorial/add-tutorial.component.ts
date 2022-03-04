import { Component, OnInit } from '@angular/core';
import { TutorialService } from 'src/app/services/tutorial.service';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-add-tutorial',
  templateUrl: './add-tutorial.component.html',
  styleUrls: ['./add-tutorial.component.css']
})
export class AddTutorialComponent implements OnInit {
  tutorial = {
    object: '',
    description: '',
    row: '',
    columm:'',
    condition: '',
    state: ''
  };
  submitted = false;

  constructor(private tutorialService: TutorialService, private http: HttpClient) { }

  ngOnInit(): void {
  }

  saveTutorial(): void {
    
    const data = {
      object: this.tutorial.object,
      description: this.tutorial.description,
      row: this.tutorial.row,
      columm: this.tutorial.columm,
      condition: this.tutorial.condition,
      state: this.tutorial.state,
    };
    this.tutorialService.create(data)
      .subscribe(
        response => {
          console.log(response);
          this.submitted = true;
        },
        error => {
          console.log(error);
        });

  }

  newTutorial(): void {
    this.submitted = false;
    this.tutorial = {
      object: '',
      description: '',
      row:'',
      columm:'',
      condition: '',
      state: ''
    };
  }

}
