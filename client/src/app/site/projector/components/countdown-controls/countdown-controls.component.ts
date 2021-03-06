import { Component, Input } from '@angular/core';
import { Title } from '@angular/platform-browser';
import { MatSnackBar } from '@angular/material';

import { TranslateService } from '@ngx-translate/core';

import { BaseViewComponent } from '../../../base/base-view';
import { ViewCountdown } from '../../models/view-countdown';
import { CountdownRepositoryService } from 'app/core/repositories/projector/countdown-repository.service';
import { ConfigService } from 'app/core/ui-services/config.service';

@Component({
    selector: 'os-countdown-controls',
    templateUrl: './countdown-controls.component.html'
})
export class CountdownControlsComponent extends BaseViewComponent {
    @Input()
    public countdown: ViewCountdown;

    /**
     * The time in seconds to make the countdown orange, is the countdown is below this value.
     */
    public warningTime: number;

    public constructor(
        titleService: Title,
        translate: TranslateService,
        matSnackBar: MatSnackBar,
        private repo: CountdownRepositoryService,
        private configService: ConfigService
    ) {
        super(titleService, translate, matSnackBar);

        this.configService.get<number>('agenda_countdown_warning_time').subscribe(time => (this.warningTime = time));
    }

    /**
     * Start the countdown
     */
    public start(event: Event): void {
        event.stopPropagation();
        this.repo.start(this.countdown).catch(this.raiseError);
    }

    /**
     * Pause the countdown
     */
    public pause(event: Event): void {
        event.stopPropagation();
        this.repo.pause(this.countdown).catch(this.raiseError);
    }

    /**
     * Stop the countdown
     */
    public stop(event: Event): void {
        event.stopPropagation();
        this.repo.stop(this.countdown).catch(this.raiseError);
    }

    /**
     * One can stop the countdown, if it is running or not resetted.
     */
    public canStop(): boolean {
        return this.countdown.running || this.countdown.countdown_time !== this.countdown.default_time;
    }
}
