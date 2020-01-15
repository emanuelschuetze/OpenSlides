import { Component, OnInit } from '@angular/core';
import { MatSnackBar } from '@angular/material';
import { Title } from '@angular/platform-browser';
import { ActivatedRoute, Router } from '@angular/router';

import { TranslateService } from '@ngx-translate/core';

import { MotionPollRepositoryService } from 'app/core/repositories/motions/motion-poll-repository.service';
import { GroupRepositoryService } from 'app/core/repositories/users/group-repository.service';
import { PromptService } from 'app/core/ui-services/prompt.service';
import { ViewMotionPoll } from 'app/site/motions/models/view-motion-poll';
import { MotionPollDialogService } from 'app/site/motions/services/motion-poll-dialog.service';
import { BasePollDetailComponent } from 'app/site/polls/components/base-poll-detail.component';
// import { MotionRepositoryService } from 'app/core/repositories/motions/motion-repository.service';

@Component({
    selector: 'os-motion-poll-detail',
    templateUrl: './motion-poll-detail.component.html',
    styleUrls: ['./motion-poll-detail.component.scss']
})
export class MotionPollDetailComponent extends BasePollDetailComponent<ViewMotionPoll> implements OnInit {
    public chartType = 'doughnut';
    public motionTitle = '';

    public constructor(
        title: Title,
        translate: TranslateService,
        matSnackbar: MatSnackBar,
        repo: MotionPollRepositoryService,
        route: ActivatedRoute,
        groupRepo: GroupRepositoryService,
        prompt: PromptService,
        pollDialog: MotionPollDialogService,
        private router: Router // private motionRepo: MotionRepositoryService
    ) {
        super(title, translate, matSnackbar, repo, route, groupRepo, prompt, pollDialog);
    }

    public ngOnInit(): void {
        // this.motionTitle = this.motionRepo.getViewModel((<ViewMotionPoll>this.poll).motion_id).getTitle();
    }

    public openDialog(): void {
        this.pollDialog.openDialog(this.poll);
    }

    protected onDeleted(): void {
        this.router.navigate(['motions', (<ViewMotionPoll>this.poll).motion_id]);
    }
}
