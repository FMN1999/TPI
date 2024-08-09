import { ComponentFixture, TestBed } from '@angular/core/testing';

import { AltaLigaComponent } from './alta-liga.component';

describe('AltaLigaComponent', () => {
  let component: AltaLigaComponent;
  let fixture: ComponentFixture<AltaLigaComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [AltaLigaComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(AltaLigaComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
