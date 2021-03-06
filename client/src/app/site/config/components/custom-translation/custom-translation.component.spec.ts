import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { CustomTranslationComponent } from './custom-translation.component';
import { E2EImportsModule } from 'e2e-imports.module';

describe('CustomTranslationComponent', () => {
    let component: CustomTranslationComponent;
    let fixture: ComponentFixture<CustomTranslationComponent>;

    beforeEach(async(() => {
        TestBed.configureTestingModule({
            imports: [E2EImportsModule],
            declarations: [CustomTranslationComponent]
        }).compileComponents();
    }));

    beforeEach(() => {
        fixture = TestBed.createComponent(CustomTranslationComponent);
        component = fixture.componentInstance;
        fixture.detectChanges();
    });

    it('should create', () => {
        expect(component).toBeTruthy();
    });
});
