import { ComponentFixture, TestBed } from '@angular/core/testing';

import { DemoSensor } from './demo-sensor';

describe('DemoSensor', () => {
  let component: DemoSensor;
  let fixture: ComponentFixture<DemoSensor>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [DemoSensor],
    }).compileComponents();

    fixture = TestBed.createComponent(DemoSensor);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
