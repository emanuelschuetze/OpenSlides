import { TestBed, async, fakeAsync, tick } from '@angular/core/testing';
import { AppComponent } from './app.component';
import { E2EImportsModule } from './../e2e-imports.module';
import { ServertimeService } from './core/core-services/servertime.service';
import { TranslateService } from '@ngx-translate/core';

describe('AppComponent', () => {
    let servertimeService, translate;

    beforeEach(async(() => {
        TestBed.configureTestingModule({
            imports: [E2EImportsModule]
        }).compileComponents();

        servertimeService = TestBed.get(ServertimeService);
        translate = TestBed.get(TranslateService);
        spyOn(servertimeService, 'startScheduler').and.stub();
        spyOn(translate, 'addLangs').and.stub();
        spyOn(translate, 'setDefaultLang').and.stub();
        spyOn(translate, 'getBrowserLang').and.stub();
        spyOn(translate, 'getLangs').and.returnValue([]);
        spyOn(translate, 'use').and.stub();
    }));
    it('should create the app', fakeAsync(() => {
        const fixture = TestBed.createComponent(AppComponent);
        const app = fixture.debugElement.componentInstance;
        expect(app).toBeTruthy();
        tick();
        fixture.whenStable().then(() => {
            expect(servertimeService.startScheduler).toHaveBeenCalled();
        });
    }));
});
