import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { PersonalNoteComponent } from './personal-note.component';
import { E2EImportsModule } from 'e2e-imports.module';

describe('PersonalNoteComponent', () => {
    let component: PersonalNoteComponent;
    let fixture: ComponentFixture<PersonalNoteComponent>;

    beforeEach(async(() => {
        TestBed.configureTestingModule({
            imports: [E2EImportsModule],
            declarations: [PersonalNoteComponent]
        }).compileComponents();
    }));

    beforeEach(() => {
        fixture = TestBed.createComponent(PersonalNoteComponent);
        component = fixture.componentInstance;
        fixture.detectChanges();
    });

    it('should create', () => {
        expect(component).toBeTruthy();
    });
});
