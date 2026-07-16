import { ComponentFixture, TestBed } from '@angular/core/testing';

import { DemoEstilos } from './demo-estilos';

describe('DemoEstilos', () => {
  let component: DemoEstilos;
  let fixture: ComponentFixture<DemoEstilos>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [DemoEstilos],
    }).compileComponents();

    fixture = TestBed.createComponent(DemoEstilos);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
