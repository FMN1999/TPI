import { ComponentFixture, TestBed } from '@angular/core/testing';

import { VerLigasComponent } from './ver-ligas.component';

describe('VerLigasComponent', () => {
  let component: VerLigasComponent;
  let fixture: ComponentFixture<VerLigasComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [VerLigasComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(VerLigasComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
